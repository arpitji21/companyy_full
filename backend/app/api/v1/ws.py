import asyncio
import logging
import time

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from jose import JWTError

from app.core.security import decode_token
from app.db.session import SessionLocal
from app.repositories.user_repository import UserRepository
from app.websocket.manager import manager

logger = logging.getLogger("orbit.websocket")

router = APIRouter(tags=["Realtime"])

# Client is expected to send a text "ping" this often; if none arrives
# within INTERVAL + GRACE we treat the socket as dead. This also doubles as
# the mechanism that keeps the connection warm through Render's proxy and
# any intermediate load balancers, which will silently drop a WebSocket
# that's been idle too long.
HEARTBEAT_INTERVAL_SECONDS = 25
HEARTBEAT_GRACE_SECONDS = 10

AUTH_FAILED_CLOSE_CODE = 4401
TOKEN_EXPIRING_CLOSE_CODE = 4402


def _authenticate(token: str | None) -> tuple[str | None, float | None]:
    """Validate the access token and return (user_id, exp), or (None, None).

    Uses its own short-lived DB session rather than a request-scoped
    `Depends(get_db)` — that dependency would otherwise hold a pooled
    connection checked out for the *entire lifetime of the socket* (this
    route can stay open for hours), starving the pool for ordinary HTTP
    requests. We only need the database for this one lookup, so we open and
    close it here.
    """
    if not token:
        return None, None
    try:
        payload = decode_token(token)
    except JWTError:
        return None, None
    if payload.get("type") != "access":
        return None, None

    db = SessionLocal()
    try:
        user = UserRepository(db).get(payload["sub"])
    finally:
        db.close()
    if not user or not user.is_active:
        return None, None
    return user.id, payload.get("exp")


@router.websocket("/ws/notifications")
async def notifications_socket(websocket: WebSocket, token: str | None = None):
    # Browsers can't set custom headers on a WebSocket handshake, so the
    # access token travels as a query param instead of an Authorization
    # header. It's short-lived (30 min) and this is wss:// in production,
    # so this is the standard pattern for browser WS auth.
    user_id, exp = _authenticate(token)
    if not user_id:
        await websocket.close(code=AUTH_FAILED_CLOSE_CODE, reason="Invalid or missing token")
        return

    await websocket.accept()
    await manager.connect(user_id, websocket)
    logger.info("ws connect user=%s local_connections=%s", user_id, manager.local_connection_count())

    async def close_before_token_expires() -> None:
        if not exp:
            return
        # Close ~15s ahead of actual expiry rather than waiting for it: this
        # gives the client's reconnect logic (which refreshes its access
        # token first, see useNotificationSocket.ts) a head start, so it
        # always wins the race against the token simply going stale.
        delay = max(exp - time.time() - 15, 0)
        await asyncio.sleep(delay)
        await websocket.close(code=TOKEN_EXPIRING_CLOSE_CODE, reason="Token expiring, reconnect with a fresh one")

    expiry_task = asyncio.create_task(close_before_token_expires())
    try:
        while True:
            try:
                raw = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=HEARTBEAT_INTERVAL_SECONDS + HEARTBEAT_GRACE_SECONDS,
                )
            except asyncio.TimeoutError:
                # No client heartbeat arrived in time — most likely a
                # half-open connection (laptop slept, wifi dropped, mobile
                # network switched) that the OS/proxy hasn't noticed yet.
                # Close it so it doesn't linger in the manager forever, and
                # so the client's own reconnect logic kicks in promptly.
                await websocket.close(code=status.WS_1001_GOING_AWAY, reason="Heartbeat timeout")
                break
            if raw == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        pass
    finally:
        expiry_task.cancel()
        await manager.disconnect(user_id, websocket)
        logger.info("ws disconnect user=%s local_connections=%s", user_id, manager.local_connection_count())
