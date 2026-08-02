import { useEffect, useRef } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { notificationsSocketUrl, refreshSession, tokens, type NotificationRead, type Page } from "@/lib/orbit-api";

/**
 * Real-time notification push, layered on top of the existing
 * REST + react-query setup rather than replacing it:
 *
 * - The WebSocket is treated as a low-latency *nudge*, not a guaranteed
 *   delivery channel. Every (re)connect triggers a REST refetch of
 *   notifications + unread-count, so a message dropped while offline (tab
 *   asleep, network blip, server redeploy) is caught by that reconciliation
 *   fetch instead of silently disappearing. Postgres is always the source
 *   of truth; the socket just tells us "go look."
 * - Reconnects with exponential backoff + jitter, capped at 30s, so a
 *   backend restart or blip doesn't hammer the server with reconnect
 *   attempts across every open tab at once.
 * - The server proactively closes ~15s before the access token expires
 *   (close code 4402). On that code specifically, we refresh the session
 *   first and then reconnect with the new token, instead of just retrying
 *   the same soon-to-be-rejected one.
 * - A heartbeat "ping" is sent every 20s so idling proxies (Render's, most
 *   corporate ones) don't silently drop the connection for inactivity.
 */
export function useNotificationSocket(enabled: boolean) {
  const qc = useQueryClient();
  const reconnectAttempt = useRef(0);
  const reconnectTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const heartbeatTimer = useRef<ReturnType<typeof setInterval> | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const stoppedRef = useRef(false);

  useEffect(() => {
    if (!enabled) return;
    stoppedRef.current = false;

    const reconcile = () => {
      void qc.invalidateQueries({ queryKey: ["notifications"] });
      void qc.invalidateQueries({ queryKey: ["ceo-dashboard"] });
    };

    const bumpUnreadCount = (delta: number) => {
      qc.setQueryData<Record<string, number> | undefined>(["notifications", "unread-count"], (current) =>
        current ? { ...current, unread_count: Math.max(0, (current.unread_count ?? 0) + delta) } : current,
      );
    };

    const scheduleReconnect = () => {
      if (stoppedRef.current) return;
      const attempt = reconnectAttempt.current++;
      const base = Math.min(1000 * 2 ** attempt, 30_000);
      const jitter = Math.random() * Math.min(1000, base);
      reconnectTimer.current = setTimeout(connect, base + jitter);
    };

    const connect = async () => {
      if (stoppedRef.current) return;
      if (!tokens.access) return;

      const socket = new WebSocket(notificationsSocketUrl(tokens.access));
      socketRef.current = socket;

      socket.onopen = () => {
        reconnectAttempt.current = 0;
        // Catch up on anything created/resolved while we were disconnected.
        reconcile();
        heartbeatTimer.current = setInterval(() => {
          if (socket.readyState === WebSocket.OPEN) socket.send("ping");
        }, 20_000);
      };

      socket.onmessage = (raw) => {
        let msg: { kind?: string; notification?: NotificationRead } | null = null;
        try {
          msg = JSON.parse(raw.data);
        } catch {
          return; // "pong" and anything non-JSON is just a heartbeat reply
        }
        if (msg?.kind === "notification.created" && msg.notification) {
          // Immediate UI update; reconcile() below still runs on the next
          // connect/focus as a safety net in case this or another event
          // was ever missed.
          qc.setQueryData<Page<NotificationRead> | undefined>(["notifications"], (current) =>
            current
              ? { ...current, items: [msg!.notification!, ...current.items], total: current.total + 1 }
              : current,
          );
          bumpUnreadCount(1);
          void qc.invalidateQueries({ queryKey: ["ceo-dashboard"] });
        } else if (msg?.kind === "notification.resolved") {
          reconcile();
        }
      };

      socket.onclose = async (event) => {
        if (heartbeatTimer.current) clearInterval(heartbeatTimer.current);
        if (stoppedRef.current) return;

        if (event.code === 4402) {
          // Server closed us ahead of token expiry — refresh, then
          // reconnect immediately rather than backing off.
          const refreshed = await refreshSession();
          if (refreshed) {
            reconnectAttempt.current = 0;
            void connect();
            return;
          }
        }
        if (event.code === 4401) {
          // Token was rejected outright (not just "about to expire").
          // Reconnecting with the same token would just loop; wait for the
          // next explicit sign-in instead.
          return;
        }
        scheduleReconnect();
      };

      socket.onerror = () => socket.close();
    };

    void connect();

    // Reconnect promptly (rather than waiting out backoff) when the tab
    // regains focus or the browser reports the network is back — the two
    // most common cases where a stale backoff timer would otherwise leave
    // notifications silently stale for a while.
    const onFocusOrOnline = () => {
      if (socketRef.current?.readyState !== WebSocket.OPEN) {
        if (reconnectTimer.current) clearTimeout(reconnectTimer.current);
        reconnectAttempt.current = 0;
        void connect();
      }
    };
    window.addEventListener("focus", onFocusOrOnline);
    window.addEventListener("online", onFocusOrOnline);

    return () => {
      stoppedRef.current = true;
      window.removeEventListener("focus", onFocusOrOnline);
      window.removeEventListener("online", onFocusOrOnline);
      if (reconnectTimer.current) clearTimeout(reconnectTimer.current);
      if (heartbeatTimer.current) clearInterval(heartbeatTimer.current);
      socketRef.current?.close();
      socketRef.current = null;
    };
  }, [enabled, qc]);
}
