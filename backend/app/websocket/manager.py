import asyncio
import logging
from collections import defaultdict

from fastapi import WebSocket

logger = logging.getLogger("orbit.websocket")


class ConnectionManager:
    """Tracks WebSocket connections that terminate on *this* process.

    A single user can have several simultaneous connections — a couple of
    browser tabs, a laptop and a phone — so we key by user_id and fan a
    message out to every socket that user currently has open on this
    instance. This class is intentionally single-process: it never talks to
    other backend instances. Cross-instance fan-out (user connected to
    instance B, notification created by a request handled on instance A) is
    handled one layer up, by the Redis subscriber in listener.py, which
    calls send_to_user() once the event reaches this process.
    """

    def __init__(self) -> None:
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, user_id: str, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections[user_id].add(websocket)

    async def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        async with self._lock:
            sockets = self._connections.get(user_id)
            if not sockets:
                return
            sockets.discard(websocket)
            if not sockets:
                del self._connections[user_id]

    async def send_to_user(self, user_id: str, payload: dict) -> int:
        """Push payload to every local connection for user_id.

        Returns the number of local sockets it reached. 0 is a normal,
        expected result — it just means this user isn't connected to *this*
        instance right now (they may be connected elsewhere, or simply
        offline; either way the notification is already durable in
        Postgres, so nothing is lost).
        """
        sockets = list(self._connections.get(user_id, ()))
        delivered = 0
        for ws in sockets:
            try:
                await ws.send_json(payload)
                delivered += 1
            except Exception:
                logger.debug("Dropping dead socket for user=%s", user_id, exc_info=False)
                await self.disconnect(user_id, ws)
        return delivered

    def local_connection_count(self) -> int:
        return sum(len(sockets) for sockets in self._connections.values())


# One instance per process, shared by the WS route and the Redis listener.
manager = ConnectionManager()
