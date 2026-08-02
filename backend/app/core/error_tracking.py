from app.core.config import settings
from app.core.logging import logger


def setup_sentry() -> None:
    """Initialize Sentry error tracking, if configured.

    No-ops when SENTRY_DSN isn't set (e.g. local dev, tests, CI) so this is
    always safe to call — the app behaves exactly as it did before Sentry
    was added until a real DSN is provided via the environment.
    """
    if not settings.SENTRY_DSN:
        return

    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.starlette import StarletteIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration
    except ImportError:  # pragma: no cover - sentry-sdk is in requirements.txt
        logger.warning("SENTRY_DSN is set but sentry-sdk isn't installed; skipping error tracking setup.")
        return

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
        profiles_sample_rate=settings.SENTRY_PROFILES_SAMPLE_RATE,
        send_default_pii=False,
        integrations=[
            StarletteIntegration(transaction_style="endpoint"),
            FastApiIntegration(transaction_style="endpoint"),
            # Breadcrumbs from our own logger at INFO+, and auto-capture any
            # ERROR-level (or above) log record as a Sentry event, in
            # addition to the exceptions we already report explicitly.
            LoggingIntegration(level=None, event_level="ERROR"),
        ],
    )
    logger.info("Sentry error tracking initialized (environment=%s).", settings.ENVIRONMENT)
