"""add customer, procurement, clinical, investor, tender, analytics tables

Revision ID: ddb20ae72d74
Revises: f03f6a275688
Create Date: 2026-07-30

Closes out the last 6 departments in the roadmap: Customer, Procurement,
Clinical, Investor, Tender, and Analytics. `reports` is included here too
— the `Report` model has existed in app/models/document.py since the Docs
migration (f03f6a275688) but was intentionally left out of that pass and
called out as belonging to Analytics instead. This is its first migration.

Like every other table in this repo, these were modeled in app/models/*
well before being migrated, so this is a straightforward create-tables
pass with no data to backfill.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ddb20ae72d74"
down_revision = "f03f6a275688"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- Customer ---
    op.create_table(
        "support_tickets",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.Column("customer_id", sa.String(), nullable=True),
        sa.Column("account_owner_id", sa.String(), nullable=True),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="open"),
        sa.Column("priority", sa.String(length=20), nullable=False, server_default="medium"),
        sa.Column("sla_due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("escalated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("csat_score", sa.Numeric(3, 2), nullable=True),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["account_owner_id"], ["employees.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_support_tickets_id", "support_tickets", ["id"])

    # --- Procurement ---
    op.create_table(
        "purchase_orders",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.Column("vendor_id", sa.String(), nullable=True),
        sa.Column("requested_by_id", sa.String(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="requested"),
        sa.Column("amount", sa.Numeric(14, 2), nullable=True),
        sa.Column("requested_date", sa.Date(), nullable=True),
        sa.Column("approved_date", sa.Date(), nullable=True),
        sa.Column("delivery_date", sa.Date(), nullable=True),
        sa.Column("contract_end_date", sa.Date(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["vendor_id"], ["vendors.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["requested_by_id"], ["employees.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_purchase_orders_id", "purchase_orders", ["id"])

    # --- Clinical ---
    op.create_table(
        "clinical_trials",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.Column("lead_employee_id", sa.String(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("phase", sa.String(length=10), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="planning"),
        sa.Column("site", sa.String(length=255), nullable=True),
        sa.Column("target_enrollment", sa.Integer(), nullable=True),
        sa.Column("actual_enrollment", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(["lead_employee_id"], ["employees.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_clinical_trials_id", "clinical_trials", ["id"])

    op.create_table(
        "clinical_events",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.Column("trial_id", sa.String(), nullable=True),
        sa.Column("event_type", sa.String(length=30), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False, server_default="mild"),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="open"),
        sa.Column("reported_date", sa.Date(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["trial_id"], ["clinical_trials.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_clinical_events_id", "clinical_events", ["id"])

    # --- Investor ---
    op.create_table(
        "funding_rounds",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.Column("round_name", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="planned"),
        sa.Column("amount_raised", sa.Numeric(14, 2), nullable=True),
        sa.Column("pre_money_valuation", sa.Numeric(16, 2), nullable=True),
        sa.Column("post_money_valuation", sa.Numeric(16, 2), nullable=True),
        sa.Column("lead_investor", sa.String(length=255), nullable=True),
        sa.Column("close_date", sa.Date(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_funding_rounds_id", "funding_rounds", ["id"])

    op.create_table(
        "investor_updates",
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
        sa.Column("update_type", sa.String(length=30), nullable=False, server_default="investor_update"),
        sa.Column("sent_date", sa.Date(), nullable=True),
        sa.Column("next_report_due_date", sa.Date(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_investor_updates_id", "investor_updates", ["id"])

    # --- Tender ---
    op.create_table(
        "tenders",
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
        sa.Column("client_name", sa.String(length=255), nullable=True),
        sa.Column("client_segment", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="draft"),
        sa.Column("bid_value", sa.Numeric(14, 2), nullable=True),
        sa.Column("win_probability", sa.Numeric(5, 2), nullable=True),
        sa.Column("submission_deadline", sa.Date(), nullable=True),
        sa.Column("outcome_date", sa.Date(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tenders_id", "tenders", ["id"])

    # --- Analytics (Report existed unmigrated since the Docs pass) ---
    op.create_table(
        "reports",
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
        sa.Column("department_id", sa.String(), nullable=True),
        sa.Column("report_type", sa.String(length=50), nullable=False),
        sa.Column("period_start", sa.String(length=20), nullable=True),
        sa.Column("period_end", sa.String(length=20), nullable=True),
        sa.Column("generated_by", sa.String(), nullable=True),
        sa.Column("s3_key", sa.String(length=1000), nullable=True),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["generated_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reports_id", "reports", ["id"])


def downgrade() -> None:
    op.drop_index("ix_reports_id", table_name="reports")
    op.drop_table("reports")

    op.drop_index("ix_tenders_id", table_name="tenders")
    op.drop_table("tenders")

    op.drop_index("ix_investor_updates_id", table_name="investor_updates")
    op.drop_table("investor_updates")
    op.drop_index("ix_funding_rounds_id", table_name="funding_rounds")
    op.drop_table("funding_rounds")

    op.drop_index("ix_clinical_events_id", table_name="clinical_events")
    op.drop_table("clinical_events")
    op.drop_index("ix_clinical_trials_id", table_name="clinical_trials")
    op.drop_table("clinical_trials")

    op.drop_index("ix_purchase_orders_id", table_name="purchase_orders")
    op.drop_table("purchase_orders")

    op.drop_index("ix_support_tickets_id", table_name="support_tickets")
    op.drop_table("support_tickets")
