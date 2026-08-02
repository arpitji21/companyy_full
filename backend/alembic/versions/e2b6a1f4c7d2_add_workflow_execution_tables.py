"""add workflow execution tables (steps column, workflow_runs, workflow_step_runs)

Revision ID: e2b6a1f4c7d2
Revises: 7a9f2c4e8b1d
Create Date: 2026-08-01

The `Workflow` table has existed since the baseline migration, but only
held metadata (name, trigger_type, schedule_cron) — nothing about what a
workflow actually *does*. This adds:
  - `workflows.steps`: an ordered JSON list of step definitions
  - `workflow_runs`: one row per manual trigger of a workflow
  - `workflow_step_runs`: one row per step of a run, so a run's detail view
    shows exactly which step failed and why

This is the minimal workflow engine: linear execution, manual trigger only
— no branching, scheduling, or event triggers yet (see app/tasks/workflows.py).
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e2b6a1f4c7d2"
down_revision = "7a9f2c4e8b1d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "workflows",
        sa.Column("steps", sa.JSON(), nullable=False, server_default="[]"),
    )

    op.create_table(
        "workflow_runs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.Column("workflow_id", sa.String(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("triggered_by", sa.String(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["workflow_id"], ["workflows.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["triggered_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_runs_id", "workflow_runs", ["id"])

    op.create_table(
        "workflow_step_runs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.Column("workflow_run_id", sa.String(), nullable=False),
        sa.Column("step_index", sa.Integer(), nullable=False),
        sa.Column("step_name", sa.String(length=255), nullable=False),
        sa.Column("step_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column("output", sa.JSON(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["workflow_run_id"], ["workflow_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_workflow_step_runs_id", "workflow_step_runs", ["id"])


def downgrade() -> None:
    op.drop_index("ix_workflow_step_runs_id", table_name="workflow_step_runs")
    op.drop_table("workflow_step_runs")

    op.drop_index("ix_workflow_runs_id", table_name="workflow_runs")
    op.drop_table("workflow_runs")

    op.drop_column("workflows", "steps")
