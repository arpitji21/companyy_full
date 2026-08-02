from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class SupportTicket(UUIDPKMixin, TimestampMixin, Base):
    """Post-sale support/success tickets. Distinct from Sales' pipeline —
    this is what keeps an existing `Customer` happy after they've signed,
    not what gets them to sign in the first place."""

    __tablename__ = "support_tickets"

    customer_id: Mapped[str | None] = mapped_column(
        ForeignKey("customers.id", ondelete="SET NULL"), nullable=True
    )
    account_owner_id: Mapped[str | None] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )

    subject: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="open")  # open, pending, escalated, resolved, closed
    priority: Mapped[str] = mapped_column(String(20), default="medium")  # low, medium, high, urgent

    sla_due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    escalated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    csat_score: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), nullable=True)  # 1-5, filled on close

    customer: Mapped["Customer | None"] = relationship()  # noqa: F821
