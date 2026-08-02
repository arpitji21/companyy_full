from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class FundingRound(UUIDPKMixin, TimestampMixin, Base):
    """One row per funding round. A full cap table (per-shareholder
    ownership) isn't modeled yet — this gives round-level valuation and
    ownership-dilution history, which is what the summary/API surface
    needs first."""

    __tablename__ = "funding_rounds"

    round_name: Mapped[str] = mapped_column(String(100))  # Seed, Series A, Series B, ...
    status: Mapped[str] = mapped_column(String(20), default="planned")  # planned, in_progress, closed
    amount_raised: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    pre_money_valuation: Mapped[Decimal | None] = mapped_column(Numeric(16, 2), nullable=True)
    post_money_valuation: Mapped[Decimal | None] = mapped_column(Numeric(16, 2), nullable=True)
    lead_investor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    close_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


class InvestorUpdate(UUIDPKMixin, TimestampMixin, Base):
    """Shared feed for investor updates and board meeting minutes —
    differentiated by `update_type` so the archive reads as one
    chronological log."""

    __tablename__ = "investor_updates"

    title: Mapped[str] = mapped_column(String(255))
    update_type: Mapped[str] = mapped_column(String(30), default="investor_update")  # investor_update, board_minutes
    sent_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    next_report_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
