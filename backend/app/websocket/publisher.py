import json
import logging

import redis

from app.core.config import settings

logger = logging.getLogger("orbit.websocket")

CHANNEL = "orbit:notifications"

# NotificationService runs on the normal sync request path (sync SQLAlchemy
# Session), so publishing has to be sync too — a plain `redis.Redis` publish
# is a single fast round trip and safe to do inline. The async subscriber
# side (listener.py) is a separate, long-lived connection per process.
_client: "redis.Redis | None" = None


def _get_client() -> "redis.Redis | None":
    global _client
    if _client is None:
        try:
            _client = redis.Redis.from_url(
                settings.REDIS_URL, socket_timeout=1, socket_connect_timeout=1
            )
        except Exception:
            logger.warning("Could not construct Redis client for notification push.", exc_info=False)
            return None
    return _client


def publish_notification(user_id: str, event: dict) -> None:
    """Best-effort real-time push.

    Notifications are always persisted to Postgres first (see
    NotificationService) — this is purely a low-latency nudge so an open tab
    updates instantly instead of waiting for its next poll. If Redis is
    down or unreachable we log and no-op rather than raise: a dropped push
    just means the client picks the notification up on its next poll or
    reconnect fetch instead of instantly. It never means a lost
    notification, since the row is already committed.
    """
    client = _get_client()
    if client is None:
        return
    try:
        client.publish(CHANNEL, json.dumps({"user_id": user_id, "event": event}))
    except Exception:
        # Connection may have gone stale (Redis restart, network blip) —
        # drop the cached client so the next call rebuilds it instead of
        # repeatedly failing against a dead connection.
        global _client
        _client = None
        logger.warning("Redis publish failed for notification push.", exc_info=False)
