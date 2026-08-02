"""add reference_type/reference_id to notifications

Revision ID: 7a9f2c4e8b1d
Revises: ddb20ae72d74
Create Date: 2026-07-30

Lets a notification point back at the record it's about (e.g.
reference_type="approval", reference_id=<Approval.id>) so the CEO can act
on it inline from the notification/action-center feed instead of having to
navigate to the owning department's page. Same caveat as the other Phase 1
tables (see f03f6a275688): `notifications` itself predates alembic in this
repo and is only ever created via Base.metadata.create_all today, so this
migration only applies cleanly once that table exists.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7a9f2c4e8b1d"
down_revision = "ddb20ae72d74"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("notifications", sa.Column("reference_type", sa.String(length=50), nullable=True))
    op.add_column("notifications", sa.Column("reference_id", sa.String(length=64), nullable=True))


def downgrade() -> None:
    op.drop_column("notifications", "reference_id")
    op.drop_column("notifications", "reference_type")
