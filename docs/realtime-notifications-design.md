# Real-time notifications — design notes

## Starting point

The `notifications` table, REST endpoints (`GET /notifications`,
`GET /notifications/unread-count`, `POST /notifications/{id}/read`), and
`NotificationService` (including the `notify_role` fan-out used by
approvals, etc.) already existed and are unchanged in shape. The only gap
was delivery: the frontend fetched once on mount and otherwise only
refreshed on a manual `invalidateQueries` after an action the user
themselves took. Another user's action (someone else approving something,
a workflow creating a notification) never showed up until a manual reload.
`app/websocket/` existed as an empty package with nothing in it.

This doc covers the three things that needed actual design work, in order.

## 1. Connection management

`app/websocket/manager.py` — `ConnectionManager` is a plain in-process
registry: `dict[user_id, set[WebSocket]]`, guarded by an `asyncio.Lock`
for the add/remove paths (`send_to_user` iterates a snapshot list, so it
doesn't need the lock — a socket removed mid-broadcast just fails its
`send_json` and gets cleaned up).

Key decisions:

- **Keyed by user, not by connection.** A user can have several sockets at
  once (two browser tabs, phone + laptop), and every one of them should
  get every notification meant for that user. `send_to_user` fans out to
  all of them.
- **Dead sockets self-heal.** If `send_json` raises (socket already
  closed, network reset), the manager drops that socket from its set right
  there rather than waiting for the WS route's own disconnect handler to
  eventually run. One broken tab can't poison delivery to the user's other
  tabs.
- **Strictly single-process.** This class knows nothing about other
  backend instances. That's intentional — see part 2.

## 2. Scaling across multiple servers

The hard part isn't holding a WebSocket open — Starlette/FastAPI does that
for free. It's that **the instance that creates a notification and the
instance holding the recipient's open socket are usually different
processes.** A request that triggers `notify_role(["CEO", "Admin"])` lands
on whichever instance the load balancer picked; the CEO's browser tab is
attached to whichever instance *it* was routed to when it opened the
socket. With N instances behind a load balancer, there's roughly a
`(N-1)/N` chance those are two different processes — the more instances,
the more this matters. An in-memory-only `ConnectionManager` would silently
drop most cross-instance notifications.

The fix is Redis pub/sub as the shared layer every instance already has
access to (it's already provisioned for Celery, just unused until now):

- **`publisher.py`** — a synchronous `redis.Redis.publish()` call, invoked
  from `NotificationService` immediately after each notification commits
  (`create`, the loop in `notify_role`, and `resolve_reference`). Sync
  because the service layer runs on FastAPI's sync request path with a
  sync SQLAlchemy `Session` — no event loop to hand an async publish to
  without extra machinery that would buy nothing here, since a Redis
  `PUBLISH` is a single fast round trip.
- **`listener.py`** — one `redis.asyncio` subscriber task per process,
  started in `main.py`'s `lifespan` and living for the process's lifetime.
  It subscribes to a single channel (`orbit:notifications`), and for every
  message calls `manager.send_to_user(user_id, event)` — reaching only the
  sockets that happen to be local to *that* process, which is exactly
  right, since pub/sub already delivered the message to every process.
- **One channel, not one per user.** With a single logical channel every
  instance subscribes once and filters locally by `user_id` in the message
  body. Per-user channels would mean subscribing/unsubscribing on every
  socket connect/disconnect, which is needless overhead at this scale (an
  internal ops tool, not a consumer chat app) and adds a class of bugs
  (subscription leaks) for no real gain.
- **Fire-and-forget by design.** The notification row is committed to
  Postgres *before* the publish call, and the publish is wrapped so a
  Redis outage or blip never raises past `NotificationService` — it logs
  and no-ops. Worst case, a push is late or missed; the frontend's
  reconciliation fetch (part 3) catches it. Redis pub/sub has no delivery
  guarantee or replay anyway (a subscriber that's down when a message is
  published never sees it), so treating the whole channel as "best-effort
  nudge, not transport" is the honest framing rather than something to
  paper over.
- **Deployment reality, called out explicitly in `render.yaml`:**
  `REDIS_URL` moved from "optional, unwired" to required-for-this-feature.
  On the current free web-service plan (single instance, no autoscaling)
  the cross-instance path isn't even exercised yet — but building it
  correctly now means turning on a second instance later is a plan change,
  not a rewrite.

## 3. Reconnect handling

A WebSocket in a browser dies constantly and for boring reasons: laptop
sleeps, wifi hands off, a corporate proxy times out an idle connection, the
backend redeploys, Render's free-tier instance spins down after 15 minutes
idle. All of that is normal operation, not an error state, and the design
treats it that way.

**Server side (`app/api/v1/ws.py`):**

- **Auth is query-param JWT**, not a header, because the browser
  `WebSocket` API has no way to set `Authorization` on the handshake. The
  existing access token (already short-lived, already used everywhere
  else) is reused as-is — no new token type.
- **Auth uses its own short-lived DB session**, not the shared
  `Depends(get_db)` used by HTTP routes. That dependency holds a pooled
  connection checked out for the full request lifetime — fine for a
  request that finishes in milliseconds, not fine for a socket that might
  stay open for hours, which would slowly starve the pool as concurrent
  sockets accumulate. The WS route opens a session, does one user lookup,
  and closes it before entering the long-lived loop.
- **App-level heartbeat.** The client sends a text `"ping"` every 20s; the
  server replies `"pong"` and otherwise waits on `receive_text()` with a
  35s timeout. No heartbeat in time closes the socket. This exists
  specifically because idling reverse proxies (Render's included) will
  silently drop a WebSocket that's gone quiet for too long — periodic
  traffic in both directions is the standard way to keep those happy, and
  the timeout also means a half-open connection (cable pulled, OS didn't
  notice) gets reclaimed instead of sitting in the `ConnectionManager`
  forever.
- **Proactive close ahead of token expiry.** On connect, the server reads
  the token's `exp` claim and schedules a close ~15s before it, using a
  distinct close code (4402) rather than just letting the token go stale
  and the *next* action silently fail. That gives the client a clean,
  unambiguous signal: "refresh, then reconnect," rather than having to
  guess why the socket died.

**Client side (`frontend/src/lib/useNotificationSocket.ts`):**

- **Exponential backoff with jitter**, capped at 30s. Jitter matters
  specifically because a backend restart drops every open socket at once —
  without jitter, every tab across every user would retry in lockstep and
  hit the freshly-restarted backend with a synchronized thundering herd
  right as it's coming back up.
- **Close code 4402 (token expiring) triggers an immediate refresh +
  reconnect**, bypassing backoff entirely — this isn't a failure, it's an
  expected handshake the server initiated on purpose.
- **Close code 4401 (auth rejected outright) stops retrying.** Looping on
  a token the server has already rejected would just spin forever; the
  next real sign-in is what fixes this, not another reconnect attempt.
- **Reconnect immediately on tab focus or `online`**, instead of waiting
  out whatever backoff delay happens to be pending. This is the difference
  between "notifications feel instant when I switch back to this tab" and
  "notifications feel stale for up to 30 seconds after."
- **Every (re)connect triggers a REST reconciliation fetch** of
  notifications + unread-count. This is the safety net underneath
  everything above: WebSocket delivery (and Redis pub/sub underneath it)
  is best-effort, so the guarantee that actually matters — "nothing stays
  permanently missed" — comes from the REST fetch on reconnect, not from
  the socket. Individual `notification.created` events are still applied
  optimistically to the query cache for instant UI feedback; the
  reconciliation fetch is what makes that safe to do without also being
  the only mechanism.

## What this deliberately does not do

- **No message queue / replay buffer for offline users.** Notifications
  already live durably in Postgres and the existing `GET /notifications`
  endpoint is the replay mechanism — building a second one on top (e.g.
  a per-user Redis stream with cursors) would duplicate that for no real
  benefit at this scale.
- **No sticky sessions / connection draining for deploys.** Out of scope
  for this task; a deploy simply closes sockets, which the reconnect logic
  already treats as a normal case. Worth revisiting if deploy-time
  notification gaps ever become a real complaint.
- **No presence / "who's online" feature**, even though the connection
  manager incidentally has enough information to build one. Not asked for.
