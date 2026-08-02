from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.error_tracking import setup_sentry
from app.core.logging import setup_logging
from app.middlewares.exception_handlers import register_exception_handlers
from app.middlewares.logging_middleware import RequestLoggingMiddleware
from app.middlewares.rate_limit_middleware import RateLimitMiddleware
from app.websocket.listener import listener


@asynccontextmanager
async def lifespan(app: FastAPI):
    # One Redis subscriber task per process — see app/websocket/listener.py
    # for why this is what makes notification push work across multiple
    # backend instances.
    await listener.start()
    try:
        yield
    finally:
        await listener.stop()


def create_app() -> FastAPI:
    setup_logging()
    setup_sentry()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        description="Backend API for the LarkAI Orbit enterprise dashboard.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    register_exception_handlers(app)

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
