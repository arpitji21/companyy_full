from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "larkai_orbit",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Modules the worker imports on startup so their @celery_app.task
    # functions get registered. Listed here (rather than imported at the
    # top of this file) so each task module can do
    # `from app.tasks.celery_app import celery_app` without a circular
    # import back into this file.
    imports=(
        "app.tasks.email",
        "app.tasks.reports",
        "app.tasks.workflows",
    ),
)
