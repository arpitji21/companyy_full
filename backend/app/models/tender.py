from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class Tender(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "tenders"

    title: Mapped[str] = mapped_column(String(255))
    client_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    client_segment: Mapped[str | None] = mapped_column(String(100), nullable=True)  # government, enterprise, ...
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, submitted, shortlisted, won, lost, withdrawn
    bid_value: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    win_probability: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)  # 0-100
    submission_deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    outcome_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)  # doubles as the submission checklist for now
