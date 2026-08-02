"""add documents table

Revision ID: f03f6a275688
Revises: a3ff2d87bec3
Create Date: 2026-07-30

The `Document` model already existed in app/models/document.py before this
department was built out, but (like every other table in this repo — see
the note on 31bb1a002cc9) it was never actually migrated. This is its
first migration. `Report` (also in document.py) isn't included yet — it
belongs to the Analytics/reporting pass, not Docs.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f03f6a275688"
down_revision = "a3ff2d87bec3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("folder", sa.String(length=255), nullable=True),
        sa.Column("department_id", sa.String(), nullable=True),
        sa.Column("uploaded_by", sa.String(), nullable=True),
        sa.Column("s3_key", sa.String(length=1000), nullable=False),
        sa.Column("mime_type", sa.String(length=100), nullable=True),
        sa.Column("size_bytes", sa.BigInteger(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("ocr_text", sa.Text(), nullable=True),
        sa.Column("ai_summary", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["uploaded_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_documents_id", "documents", ["id"])


def downgrade() -> None:
    op.drop_index("ix_documents_id", table_name="documents")
    op.drop_table("documents")
