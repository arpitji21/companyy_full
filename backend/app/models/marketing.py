from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class MarketingCampaign(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "marketing_campaigns"

    name: Mapped[str] = mapped_column(String(255))
    channel: Mapped[str] = mapped_column(String(50))  # social, email, seo, content, paid
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, scheduled, live, completed
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    budget: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    impressions: Mapped[int] = mapped_column(Integer, default=0)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    conversions: Mapped[int] = mapped_column(Integer, default=0)
    roi: Mapped[float | None] = mapped_column(Numeric(6, 2), nullable=True)


class Ticket(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "tickets"

    customer_id: Mapped[str | None] = mapped_column(ForeignKey("customers.id", ondelete="SET NULL"), nullable=True)
    subject: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="open")  # open, in_progress, resolved, closed
    priority: Mapped[str] = mapped_column(String(20), default="normal")
    assignee_id: Mapped[str | None] = mapped_column(ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
