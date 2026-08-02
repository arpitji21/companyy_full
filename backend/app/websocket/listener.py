import asyncio
import json
import logging

import redis.asyncio as aioredis

from app.core.config import settings
from app.websocket.manager import manager
from app.websocket.publisher import CHANNEL

logger = logging.getLogger("orbit.websocket")


class NotificationListener:
    """Bridges Redis pub/sub into this process's local WebSocket connections.

    Every backend instance runs exactly one of these (started from main.py's
    lifespan). A notification created by a request handled on instance A is
    published to Redis by publisher.py; every instance — A, B, C, ... —
    receives it here and forwards it to whichever of *its own* locally
    connected sockets belong to that user. This is the mechanism that makes
    horizontal scaling work: the instance that creates a notification and
    the instance holding the recipient's open WebSocket are frequently
    different processes behind the load balancer, and Redis pub/sub is the
    only channel they share.

    Reconnects with exponential backoff if Redis drops, so a transient
    Redis restart degrades to "push arrives late/not at all, REST polling
    still works" rather than crashing the listener task permanently.
    """

    def __init__(self) -> None:
        self._task: asyncio.Task | None = None
        self._redis: aioredis.Redis | None = None
        self._stopping = False

    async def start(self) -> None:
        self._stopping = False
        self._task = asyncio.create_task(self._run(), name="notification-listener")

    async def stop(self) -> None:
        self._stopping = True
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self._redis:
            await self._redis.aclose()

    async def _run(self) -> None:
        backoff = 1
        while not self._stopping:
            try:
                self._redis = aioredis.Redis.from_url(settings.REDIS_URL)
                pubsub = self._redis.pubsub()
                await pubsub.subscribe(CHANNEL)
                logger.info("Notification listener subscribed to %s", CHANNEL)
                backoff = 1  # reset once we've successfully (re)connected
                async for message in pubsub.listen():
                    if message["type"] != "message":
                        continue
                    await self._handle(message["data"])
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.warning(
                    "Notification listener lost its Redis connection, retrying in %ss", backoff, exc_info=False
                )
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 30)

    async def _handle(self, raw: bytes | str) -> None:
        try:
            data = json.loads(raw)
            await manager.send_to_user(data["user_id"], data["event"])
        except Exception:
            logger.warning("Malformed notification pub/sub message, dropping.", exc_info=False)


listener = NotificationListener()
