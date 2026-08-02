from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class Workflow(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "workflows"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    trigger_type: Mapped[str] = mapped_column(String(50))  # manual, scheduled, event
    schedule_cron: Mapped[str | None] = mapped_column(String(100), nullable=True)  # for scheduled jobs
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # Ordered list of step definitions, e.g.
    # [{"name": "Notify finance", "type": "notify_role",
    #   "config": {"role_names": ["Finance"], "title": "...", "body": "..."}}]
    # Only "manual" trigger_type actually executes anything right now (see
    # POST /workflows/{id}/run) — "scheduled"/"event" are accepted values on
    # the model for forward-compatibility but nothing schedules or fires
    # them yet.
    steps: Mapped[list] = mapped_column(JSON, default=list, server_default="[]")


class WorkflowRun(UUIDPKMixin, TimestampMixin, Base):
    """One execution of a Workflow's steps, in order, run inline inside a
    single Celery task (app/tasks/workflows.py) — no branching/parallelism,
    just a straightforward step-by-step log. That's deliberately the whole
    scope of the "minimal" engine: enough to trigger and audit a workflow
    run, without building a general-purpose orchestrator."""

    __tablename__ = "workflow_runs"

    workflow_id: Mapped[str] = mapped_column(ForeignKey("workflows.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, running, succeeded, failed
    triggered_by: Mapped[str | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)


class WorkflowStepRun(UUIDPKMixin, TimestampMixin, Base):
    """Per-step log row for a WorkflowRun — one per entry in the parent
    Workflow's `steps` list, in the same order, so a run's detail view can
    show exactly which step failed and why."""

    __tablename__ = "workflow_step_runs"

    workflow_run_id: Mapped[str] = mapped_column(ForeignKey("workflow_runs.id", ondelete="CASCADE"))
    step_index: Mapped[int] = mapped_column(Integer)
    step_name: Mapped[str] = mapped_column(String(255))
    step_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, succeeded, failed
    output: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Approval(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "approvals"

    title: Mapped[str] = mapped_column(String(255))
    requested_by: Mapped[str | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    department_id: Mapped[str | None] = mapped_column(ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, approved, rejected
    approver_id: Mapped[str | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
