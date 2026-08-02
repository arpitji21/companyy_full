import logging
import time
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.config import settings

logger = logging.getLogger("app.rate_limit")

try:
    from redis import asyncio as aioredis
except ImportError:  # pragma: no cover - redis is a hard dependency, but stay defensive
    aioredis = None


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Sliding-window rate limiter, keyed by client IP.

    Backed by Redis (sorted-set sliding window) so the limit is shared
    correctly across every worker/instance in production — an in-process
    limiter would let each worker grant its own separate quota, which
    quietly multiplies the effective limit the moment you scale past one
    process.

    Falls back to a local in-memory window (the original single-process
    behaviour) if Redis is unreachable, so a Redis outage degrades the
    limiter instead of taking the whole API down. Every request still gets
    served either way — this middleware fails open, never closed.
    """

    def __init__(self, app, requests_per_minute: int | None = None):
        super().__init__(app)
        self.limit = requests_per_minute or settings.RATE_LIMIT_PER_MINUTE
        self.window_seconds = 60
        self._redis = None
        self._redis_unavailable_logged = False

        # In-memory fallback store, used only when Redis can't be reached.
        self._local_hits: dict[str, deque] = defaultdict(deque)

        if aioredis is not None:
            try:
                self._redis = aioredis.from_url(
                    settings.REDIS_URL, decode_responses=True
                )
            except Exception:
                self._redis = None

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"

        allowed = await self._check_redis(client_ip)
        if allowed is None:
            # Redis wasn't available for this check — fall back locally.
            allowed = self._check_local(client_ip)

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"error": "rate_limited", "message": "Too many requests. Please slow down."},
            )

        return await call_next(request)

    async def _check_redis(self, client_ip: str) -> bool | None:
        """Returns True/False if Redis answered, or None if Redis is unavailable."""
        if self._redis is None:
            return None

        key = f"ratelimit:{client_ip}"
        now = time.time()
        window_start = now - self.window_seconds

        try:
            async with self._redis.pipeline(transaction=True) as pipe:
                pipe.zremrangebyscore(key, 0, window_start)
                pipe.zadd(key, {str(now): now})
                pipe.zcard(key)
                pipe.expire(key, self.window_seconds)
                _, _, count, _ = await pipe.execute()
            return count <= self.limit
        except Exception as exc:
            if not self._redis_unavailable_logged:
                logger.warning(
                    "Rate limiter could not reach Redis (%s) — "
                    "falling back to in-memory, single-process limiting.",
                    exc,
                )
                self._redis_unavailable_logged = True
            return None

    def _check_local(self, client_ip: str) -> bool:
        now = time.time()
        hits = self._local_hits[client_ip]

        while hits and now - hits[0] > self.window_seconds:
            hits.popleft()

        if len(hits) >= self.limit:
            return False

        hits.append(now)
        return True
