"""add research_projects and publications tables

Revision ID: 31bb1a002cc9
Revises: c1a5e4f9b001
Create Date: 2026-07-30

UPDATE: this now chains onto c1a5e4f9b001_add_core_baseline_tables, the
baseline migration generated via `alembic revision --autogenerate -m
"baseline"` against the full set of ~30 models, which creates the other
14 departments' tables (including `employees` and `departments`, which
this migration's FKs depend on). Verified end-to-end against a real
Postgres 16 database: `alembic upgrade head` now runs clean from an empty
database, and `alembic downgrade base` cleanly reverses the whole chain.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "31bb1a002cc9"
down_revision = "c1a5e4f9b001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "research_projects",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("field", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="planning"),
        sa.Column("lead_employee_id", sa.String(), nullable=True),
        sa.Column("department_id", sa.String(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("budget", sa.Numeric(14, 2), nullable=True),
        sa.Column("spend", sa.Numeric(14, 2), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["lead_employee_id"], ["employees.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_research_projects_id", "research_projects", ["id"])

    op.create_table(
        "publications",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.Column("research_project_id", sa.String(), nullable=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("authors", sa.String(length=500), nullable=True),
        sa.Column("journal", sa.String(length=255), nullable=True),
        sa.Column("publication_date", sa.Date(), nullable=True),
        sa.Column("doi", sa.String(length=120), nullable=True),
        sa.Column("citation_count", sa.Integer(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["research_project_id"], ["research_projects.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_publications_id", "publications", ["id"])


def downgrade() -> None:
    op.drop_index("ix_publications_id", table_name="publications")
    op.drop_table("publications")
    op.drop_index("ix_research_projects_id", table_name="research_projects")
    op.drop_table("research_projects")
