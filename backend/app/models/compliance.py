from __future__ import annotations

from datetime import date

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class ComplianceRecord(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "compliance_records"

    framework: Mapped[str] = mapped_column(String(50))  # FDA, CDSCO, ISO, MDR, GDPR, ...
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(30), default="in_progress")  # draft, submitted, approved, expired
    submission_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    certificate_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
