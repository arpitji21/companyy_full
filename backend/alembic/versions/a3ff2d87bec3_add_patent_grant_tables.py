"""add patent_filings and grant_applications tables

Revision ID: a3ff2d87bec3
Revises: 31bb1a002cc9
Create Date: 2026-07-30

Chains onto the research migration since both tables have an FK back to
research_projects.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a3ff2d87bec3"
down_revision = "31bb1a002cc9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "patent_filings",
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
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("jurisdiction", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="draft"),
        sa.Column("application_number", sa.String(length=100), nullable=True),
        sa.Column("filing_date", sa.Date(), nullable=True),
        sa.Column("grant_date", sa.Date(), nullable=True),
        sa.Column("renewal_date", sa.Date(), nullable=True),
        sa.Column("estimated_value", sa.Numeric(14, 2), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["research_project_id"], ["research_projects.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_patent_filings_id", "patent_filings", ["id"])

    op.create_table(
        "grant_applications",
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
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("funding_body", sa.String(length=150), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="draft"),
        sa.Column("amount_requested", sa.Numeric(14, 2), nullable=True),
        sa.Column("amount_awarded", sa.Numeric(14, 2), nullable=True),
        sa.Column("amount_disbursed", sa.Numeric(14, 2), nullable=False, server_default="0"),
        sa.Column("submission_date", sa.Date(), nullable=True),
        sa.Column("decision_date", sa.Date(), nullable=True),
        sa.Column("reporting_due_date", sa.Date(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["research_project_id"], ["research_projects.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_grant_applications_id", "grant_applications", ["id"])


def downgrade() -> None:
    op.drop_index("ix_grant_applications_id", table_name="grant_applications")
    op.drop_table("grant_applications")
    op.drop_index("ix_patent_filings_id", table_name="patent_filings")
    op.drop_table("patent_filings")
