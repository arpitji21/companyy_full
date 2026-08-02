"""Background email-sending tasks.

Each task builds its own subject/body and calls the low-level `send_email`
helper (app/core/email.py), which no-ops when SMTP isn't configured.
Retries a few times with backoff for transient SMTP failures (server
hiccup, rate limit) before giving up — dispatched via `app.tasks.safe_delay`
so a Celery/Redis outage never blocks the request that triggered the email.
"""
from __future__ import annotations

from app.core.config import settings
from app.core.email import send_email
from app.tasks.celery_app import celery_app

_RETRY_KWARGS = dict(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True,
    max_retries=3,
)


@celery_app.task(name="app.tasks.email.send_password_reset_email", **_RETRY_KWARGS)
def send_password_reset_email(user_email: str, user_name: str, token: str) -> None:
    link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    send_email(
        to=user_email,
        subject="Reset your LarkAI Orbit password",
        text_body=(
            f"Hi {user_name},\n\n"
            "We received a request to reset your password. This link expires in 1 hour:\n"
            f"{link}\n\n"
            "If you didn't request this, you can safely ignore this email."
        ),
        html_body=(
            f"<p>Hi {user_name},</p>"
            "<p>We received a request to reset your password. This link expires in 1 hour:</p>"
            f'<p><a href="{link}">{link}</a></p>'
            "<p>If you didn't request this, you can safely ignore this email.</p>"
        ),
    )


@celery_app.task(name="app.tasks.email.send_email_verification_email", **_RETRY_KWARGS)
def send_email_verification_email(user_email: str, user_name: str, token: str) -> None:
    link = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    send_email(
        to=user_email,
        subject="Verify your LarkAI Orbit email address",
        text_body=(
            f"Hi {user_name},\n\n"
            "Please confirm your email address by visiting this link (expires in 24 hours):\n"
            f"{link}"
        ),
        html_body=(
            f"<p>Hi {user_name},</p>"
            "<p>Please confirm your email address (this link expires in 24 hours):</p>"
            f'<p><a href="{link}">{link}</a></p>'
        ),
    )


@celery_app.task(name="app.tasks.email.send_approval_needed_email", **_RETRY_KWARGS)
def send_approval_needed_email(recipient_email: str, approval_title: str, notes: str | None) -> None:
    """One task call per recipient (rather than looping over recipients
    inside a single task) so a transient failure only retries — and only
    resends — to the one recipient it actually failed for."""
    link = f"{settings.FRONTEND_URL}/app/approvals"
    notes_text = f"\n\nNotes: {notes}" if notes else ""
    notes_html = f"<p>Notes: {notes}</p>" if notes else ""
    send_email(
        to=recipient_email,
        subject=f"Approval needed: {approval_title}",
        text_body=(
            f"A new approval needs your decision: {approval_title}.{notes_text}\n\n"
            f"Review it here: {link}"
        ),
        html_body=(
            f"<p>A new approval needs your decision: <strong>{approval_title}</strong>.</p>"
            f"{notes_html}"
            f'<p><a href="{link}">Review it here</a></p>'
        ),
    )
