from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class PatentFiling(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "patent_filings"

    research_project_id: Mapped[str | None] = mapped_column(
        ForeignKey("research_projects.id", ondelete="SET NULL"), nullable=True
    )

    title: Mapped[str] = mapped_column(String(255))
    jurisdiction: Mapped[str] = mapped_column(String(50))  # US, EU, WIPO, IN, ...
    status: Mapped[str] = mapped_column(String(30), default="draft")  # draft, filed, pending, granted, rejected, expired
    application_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    filing_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    grant_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    renewal_date: Mapped[date | None] = mapped_column(Date, nullable=True)  # next renewal/maintenance deadline
    estimated_value: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)  # portfolio/licensing value
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    research_project: Mapped["ResearchProject | None"] = relationship()  # noqa: F821
