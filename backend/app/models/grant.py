from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class GrantApplication(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "grant_applications"

    research_project_id: Mapped[str | None] = mapped_column(
        ForeignKey("research_projects.id", ondelete="SET NULL"), nullable=True
    )

    title: Mapped[str] = mapped_column(String(255))
    funding_body: Mapped[str] = mapped_column(String(150))
    status: Mapped[str] = mapped_column(String(30), default="draft")  # draft, submitted, under_review, awarded, rejected, closed
    amount_requested: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    amount_awarded: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    amount_disbursed: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    submission_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    decision_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    reporting_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)  # next reporting obligation
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    research_project: Mapped["ResearchProject | None"] = relationship()  # noqa: F821
