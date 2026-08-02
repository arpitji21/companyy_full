from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class ClinicalTrial(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "clinical_trials"

    lead_employee_id: Mapped[str | None] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )

    title: Mapped[str] = mapped_column(String(255))
    phase: Mapped[str] = mapped_column(String(10))  # I, II, III, IV
    status: Mapped[str] = mapped_column(String(30), default="planning")  # planning, recruiting, active, completed, terminated
    site: Mapped[str | None] = mapped_column(String(255), nullable=True)

    target_enrollment: Mapped[int | None] = mapped_column(Integer, nullable=True)
    actual_enrollment: Mapped[int] = mapped_column(Integer, default=0)

    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    events: Mapped[list["ClinicalEvent"]] = relationship(back_populates="trial")


class ClinicalEvent(UUIDPKMixin, TimestampMixin, Base):
    """Covers both protocol deviations and adverse events — same shape,
    different `event_type`, so they share one feed/table rather than
    forking into two nearly-identical models."""

    __tablename__ = "clinical_events"

    trial_id: Mapped[str | None] = mapped_column(
        ForeignKey("clinical_trials.id", ondelete="SET NULL"), nullable=True
    )

    event_type: Mapped[str] = mapped_column(String(30))  # protocol_deviation, adverse_event
    severity: Mapped[str] = mapped_column(String(20), default="mild")  # mild, moderate, severe, critical
    status: Mapped[str] = mapped_column(String(20), default="open")  # open, under_review, resolved
    reported_date: Mapped[date] = mapped_column(Date)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    trial: Mapped["ClinicalTrial | None"] = relationship(back_populates="events")
