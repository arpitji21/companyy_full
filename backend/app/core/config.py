from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_INSECURE_SECRET_KEY = "CHANGE_ME_IN_PRODUCTION"


class Settings(BaseSettings):
    """
    Application configuration, loaded from environment variables / .env file.
    Never hardcode secrets — everything here has a safe local-dev default
    and MUST be overridden via environment variables in production.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- App ---
    PROJECT_NAME: str = "LarkAI Orbit Backend"
    API_V1_PREFIX: str = "/api"
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = True

    # --- Security / JWT ---
    SECRET_KEY: str = _INSECURE_SECRET_KEY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- Database ---
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/larkai_orbit"
    DB_ECHO: bool = False

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def _normalize_database_url(cls, v):
        # Managed Postgres providers (Render, Railway, Heroku, etc.) hand out
        # "postgres://" or driver-less "postgresql://" URLs. SQLAlchemy needs
        # the psycopg3 driver explicitly, so rewrite the scheme if needed.
        if isinstance(v, str):
            if v.startswith("postgres://"):
                return v.replace("postgres://", "postgresql+psycopg://", 1)
            if v.startswith("postgresql://") and "+psycopg" not in v:
                return v.replace("postgresql://", "postgresql+psycopg://", 1)
        return v

    # --- Redis / Celery ---
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # --- CORS (the existing React/Vite frontend) ---
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080"

    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def _split_cors(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # --- S3 / Object storage ---
    S3_ENDPOINT_URL: str | None = None
    S3_BUCKET_NAME: str = "larkai-orbit-documents"
    S3_ACCESS_KEY: str | None = None
    S3_SECRET_KEY: str | None = None
    S3_REGION: str = "us-east-1"

    # --- File uploads / virus scanning (app/services/file_scanning.py) ---
    MAX_UPLOAD_SIZE_MB: int = 25
    # Optional — like S3/SMTP above, virus scanning still runs the fast
    # local EICAR-signature check (catches the industry-standard AV test
    # file) even with CLAMD_HOST unset, so dev/CI without a clamd container
    # still has *some* protection. Set CLAMD_HOST to scan every upload
    # against a real ClamAV daemon in staging/production.
    CLAMD_HOST: str | None = None
    CLAMD_PORT: int = 3310
    CLAMD_TIMEOUT_SECONDS: int = 15

    # --- Rate limiting ---
    RATE_LIMIT_PER_MINUTE: int = 120

    # --- Email / SMTP (used by background tasks in app/tasks/email.py) ---
    # Optional — like Sentry and the LLM provider keys below, sending mail
    # is a no-op (logged, not sent) until real SMTP credentials are set via
    # the environment. Safe to leave unset for local dev, tests, and CI.
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_USE_TLS: bool = True
    EMAILS_FROM_EMAIL: str = "no-reply@larkai-orbit.example.com"
    EMAILS_FROM_NAME: str = "LarkAI Orbit"

    # Base URL of the frontend app, used to build links in emails (password
    # reset, email verification, "review this approval", etc.).
    FRONTEND_URL: str = "http://localhost:5173"

    # --- Error tracking (Sentry) ---
    # Optional — if SENTRY_DSN is unset, Sentry is simply never initialized
    # and the app behaves exactly as before (no crash, no-op).
    SENTRY_DSN: str | None = None
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1
    SENTRY_PROFILES_SAMPLE_RATE: float = 0.0

    # --- LLM providers (Phase 4: AI Agent System) ---
    # Each is optional — an agent configured for a provider whose key is
    # missing simply returns a clear fallback message instead of crashing,
    # so the rest of the app works fine with zero keys set in dev.
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_REQUEST_TIMEOUT_SECONDS: int = 60
    DEFAULT_LLM_PROVIDER: str = "openai"

    # --- Pagination ---
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    @model_validator(mode="after")
    def _reject_insecure_secret_in_production(self) -> "Settings":
        # The placeholder SECRET_KEY is fine for local dev (docker-compose,
        # `uvicorn --reload`, tests), but must never reach a real deployment
        # since anyone who read this repo knows the value and could forge
        # JWTs with it.
        if self.ENVIRONMENT == "production" and self.SECRET_KEY == _INSECURE_SECRET_KEY:
            raise ValueError(
                "SECRET_KEY is still set to the insecure default while "
                "ENVIRONMENT=production. Set a real, random SECRET_KEY "
                "(e.g. python -c \"import secrets; print(secrets.token_urlsafe(64))\") "
                "via an environment variable before starting the app."
            )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
