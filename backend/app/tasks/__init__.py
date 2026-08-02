"""Celery task package.

`safe_delay` is the entrypoint request-handling code should use to enqueue
a background job: it swallows broker connection errors (e.g. Redis not
running in local dev, tests, or CI) so an unavailable broker never turns
into a 500 for the user — the action just doesn't happen in the
background, and a warning is logged. This mirrors every other "optional
infra" in this codebase (Sentry, LLM provider keys, SMTP) failing soft
rather than hard.
"""
from __future__ import annotations

from typing import Any

from app.core.logging import logger


def safe_delay(task: Any, *args: Any, **kwargs: Any) -> None:
    try:
        task.delay(*args, **kwargs)
    except Exception:  # broker down/unreachable, serialization error, etc.
        logger.warning(
            "Failed to enqueue background task %s; continuing without it.",
            getattr(task, "name", task),
            exc_info=True,
        )
