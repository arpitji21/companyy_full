# Deploying Orbit — Render (backend) + Vercel (frontend)

This repo is a monorepo:

```
orbit/
├── backend/     FastAPI + SQLAlchemy + Alembic + Postgres  -> deploy to Render
└── frontend/    TanStack Start (React, SSR via Nitro)       -> deploy to Vercel
```

Push this whole folder to a GitHub/GitLab repo first — both Render and Vercel
deploy from a connected git repo.

## 1. Backend → Render

A ready-to-use Blueprint is at the repo root: **`render.yaml`**. It provisions:

- A free Postgres database (`orbit-db`)
- A web service (`orbit-backend`) that runs `alembic upgrade head` then
  starts `uvicorn`, with `rootDir: backend`

### Steps

1. Go to the [Render Dashboard](https://dashboard.render.com) → **New** →
   **Blueprint**, and select this repo. Render will read `render.yaml`
   automatically.
2. Render will prompt for a few `sync: false` values — you can leave most
   blank for now and fill them in after the frontend is deployed:
   - `BACKEND_CORS_ORIGINS` — set this to your Vercel URL once you have it,
     e.g. `https://orbit-frontend.vercel.app,http://localhost:5173`
   - `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `GEMINI_API_KEY` — optional,
     only needed if you want the AI agent endpoints to actually call a
     provider (otherwise they return a graceful fallback message)
   - `S3_*` — optional, only needed for document storage
3. Click **Apply**. Render builds the backend and runs migrations
   automatically on every deploy (via `startCommand`).
4. Once live, note the backend's public URL, e.g.
   `https://orbit-backend.onrender.com` — you'll need it for step 2.
5. **Free-tier note**: Render's free web services spin down after 15 minutes
   of inactivity and take ~30-50s to wake back up on the next request. Free
   Postgres databases also expire after 30 days unless upgraded. Bump the
   `plan` fields in `render.yaml` (e.g. to `starter`) for anything beyond
   testing.

### Redis — now required (real-time notification push)

`REDIS_URL` is used by `app/websocket/` to fan notification events out
across backend instances (see `docs/realtime-notifications-design.md`).
Add a Render Key Value instance and point `REDIS_URL` at it:

```yaml
  - type: keyvalue
    name: orbit-redis
    plan: starter
    ipAllowList: []   # empty = only accessible from your Render services
```

then set `REDIS_URL` in the web service to
`fromService: { type: keyvalue, name: orbit-redis, property: connectionString }`.

Without it, the app still runs fine — a missing/unreachable Redis makes
`publish_notification()` no-op — but real-time push silently stops working
and the frontend falls back to its 60s poll for the unread badge.

On the free web-service plan (single instance, spins down after 15 minutes
idle) this is barely exercised since there's no second instance to fan out
to, but it's still worth wiring up: `GET /notifications` requests will
otherwise 500 if a route ever assumes Redis is present, and it's one less
thing to add later when you scale past one instance.

### Celery (still optional)

`CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` are wired through
`app/core/config.py`, but nothing in the codebase actually enqueues a
Celery task yet (the rate limiter is in-process, not Redis-backed). Skip
these until you add real background jobs — they can point at the same
`orbit-redis` instance above (different DB index), or a separate one. When
you do add jobs, add a worker service:

```yaml
  - type: worker
    name: orbit-celery
    runtime: python
    rootDir: backend
    buildCommand: pip install -r requirements.txt
    startCommand: celery -A app.tasks.celery_app worker --loglevel=info
    envVars:
      - key: REDIS_URL
        fromService: { type: keyvalue, name: orbit-redis, property: connectionString }
      - key: DATABASE_URL
        fromDatabase: { name: orbit-db, property: connectionString }
```

## 2. Frontend → Vercel

The frontend is a TanStack Start app (SSR via Nitro). `vite.config.ts` is
pinned to `nitro: { preset: "vercel" }` and `frontend/vercel.json` is
already set up.

### Steps

1. Go to the [Vercel Dashboard](https://vercel.com/new) → **Import
   Project** → select this repo.
2. Set **Root Directory** to `frontend` (Vercel asks for this during
   import since the repo has multiple projects).
3. Framework Preset: leave as detected / "Other" — `vercel.json` already
   sets `buildCommand` and disables auto framework detection so Vercel
   just runs `npm run build` and picks up Nitro's `.vercel/output`.
4. Add an environment variable:
   - `VITE_ORBIT_API_URL` = your Render backend URL from step 1, e.g.
     `https://orbit-backend.onrender.com`
5. Click **Deploy**.
6. Once deployed, copy the Vercel URL and go back to the Render dashboard →
   `orbit-backend` → **Environment** → set `BACKEND_CORS_ORIGINS` to that
   URL (comma-separated if you also want to allow `localhost` for local
   dev), then redeploy the backend so CORS picks it up.

## 3. Local development (unchanged)

```bash
# Backend
cd backend
cp .env.example .env
docker-compose up -d db redis   # or run Postgres/Redis yourself
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload

# Frontend
cd frontend
cp .env.example .env
npm install
npm run dev
```
