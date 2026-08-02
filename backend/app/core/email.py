"""Low-level email sending.

No-ops (logs instead of sending) when SMTP_HOST isn't configured — the same
graceful-degradation pattern used for Sentry (app/core/error_tracking.py)
and the LLM provider keys (app/core/config.py): safe to call from local
dev, tests, and CI with zero SMTP config, and only starts actually sending
mail once real credentials are set via the environment.

Exceptions from smtplib are intentionally left to propagate (not caught
here) so that Celery tasks calling this can autoretry on transient SMTP
failures instead of silently swallowing them.
"""
from __future__ import annotations

import smtplib
from email.message import EmailMessage

from app.core.config import settings
from app.core.logging import logger


def send_email(*, to: str, subject: str, text_body: str, html_body: str | None = None) -> bool:
    """Sends a single email.

    Returns True if it was actually sent, False if it was skipped because
    SMTP isn't configured — callers should treat False as a soft no-op, not
    an error, so the app behaves the same with or without SMTP set up.
    """
    if not settings.SMTP_HOST:
        logger.info("SMTP_HOST not configured; skipping email to %s (subject=%r).", to, subject)
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
    message["To"] = to
    message.set_content(text_body)
    if html_body:
        message.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as smtp:
        if settings.SMTP_USE_TLS:
            smtp.starttls()
        if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
            smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        smtp.send_message(message)

    logger.info("Sent email to %s (subject=%r).", to, subject)
    return True
