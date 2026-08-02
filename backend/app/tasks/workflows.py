"""Background workflow execution.

Runs a WorkflowRun's steps in order, inside a single Celery task, logging
each step's outcome to its own WorkflowStepRun row. This is intentionally
the whole scope of the "minimal" workflow engine: linear execution, three
built-in step actions, no branching/conditionals/scheduling yet.

Runs in a separate worker process, so it opens its own DB session
(SessionLocal) rather than reusing the request-scoped one from get_db —
same pattern as app/tasks/reports.py.
"""
from __future__ import annotations

from datetime import datetime, timezone

from app.core.email import send_email
from app.core.logging import logger
from app.db.session import SessionLocal
from app.models.workflow import WorkflowRun, WorkflowStepRun
from app.schemas.notification import NotificationCreate
from app.services.notification_service import NotificationService
from app.tasks.celery_app import celery_app


def _run_step(db, step_type: str, config: dict) -> dict:
    """Executes one step and returns a small JSON-serializable result.
    Raises on failure so the caller can record the error and stop the run."""
    if step_type == "send_notification":
        notification = NotificationService(db).create(
            NotificationCreate(
                user_id=config["user_id"],
                type=config.get("type", "workflow"),
                title=config["title"],
                body=config.get("body"),
                link=config.get("link"),
            )
        )
        return {"notification_id": notification.id}

    if step_type == "notify_role":
        created = NotificationService(db).notify_role(
            config["role_names"],
            type=config.get("type", "workflow"),
            title=config["title"],
            body=config.get("body"),
            link=config.get("link"),
        )
        return {"notification_ids": [n.id for n in created]}

    if step_type == "send_email":
        sent = send_email(
            to=config["to"],
            subject=config["subject"],
            text_body=config.get("body", ""),
            html_body=config.get("html_body"),
        )
        return {"sent": sent}

    raise ValueError(f"Unknown workflow step type: {step_type!r}")


@celery_app.task(name="app.tasks.workflows.execute_workflow_run")
def execute_workflow_run(run_id: str) -> None:
    # Imported here (not at module top) to avoid a circular import with
    # app.services.workflow_service, which imports this module lazily too.
    from app.models.workflow import Workflow

    db = SessionLocal()
    try:
        run = db.get(WorkflowRun, run_id)
        if not run:
            logger.warning("execute_workflow_run: run %s not found; skipping.", run_id)
            return

        workflow = db.get(Workflow, run.workflow_id)
        if not workflow:
            run.status = "failed"
            run.error = "Parent workflow was deleted before this run executed."
            run.finished_at = datetime.now(timezone.utc)
            db.commit()
            return

        run.status = "running"
        run.started_at = datetime.now(timezone.utc)
        db.commit()

        for index, step in enumerate(workflow.steps):
            step_run = WorkflowStepRun(
                workflow_run_id=run.id,
                step_index=index,
                step_name=step.get("name", f"Step {index + 1}"),
                step_type=step["type"],
                status="pending",
                started_at=datetime.now(timezone.utc),
            )
            db.add(step_run)
            db.commit()
            db.refresh(step_run)

            try:
                output = _run_step(db, step["type"], step.get("config", {}))
            except Exception as exc:
                step_run.status = "failed"
                step_run.error = str(exc)
                step_run.finished_at = datetime.now(timezone.utc)
                db.commit()

                run.status = "failed"
                run.error = f"Step {index + 1} ({step_run.step_name}) failed: {exc}"
                run.finished_at = datetime.now(timezone.utc)
                db.commit()
                logger.warning("Workflow run %s failed at step %s: %s", run_id, index, exc, exc_info=True)
                return

            step_run.status = "succeeded"
            step_run.output = output
            step_run.finished_at = datetime.now(timezone.utc)
            db.commit()

        run.status = "succeeded"
        run.finished_at = datetime.now(timezone.utc)
        db.commit()
    finally:
        db.close()
