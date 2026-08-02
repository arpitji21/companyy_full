from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class ManufacturingBatch(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "manufacturing_batches"

    batch_number: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    product_name: Mapped[str] = mapped_column(String(255))
    line: Mapped[str | None] = mapped_column(String(50), nullable=True)  # "Line A", "Line B"
    quantity_produced: Mapped[int] = mapped_column(Integer, default=0)
    yield_rate: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="in_progress")  # in_progress, completed, on_hold
    started_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    completed_at: Mapped[date | None] = mapped_column(Date, nullable=True)

    quality_checks: Mapped[list["QualityCheck"]] = relationship(back_populates="batch")


class QualityCheck(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "quality_checks"

    batch_id: Mapped[str | None] = mapped_column(ForeignKey("manufacturing_batches.id", ondelete="SET NULL"), nullable=True)
    check_type: Mapped[str] = mapped_column(String(50))  # CAPA, deviation, inspection, audit
    result: Mapped[str] = mapped_column(String(20), default="pending")  # pass, fail, pending
    defect_rate: Mapped[float | None] = mapped_column(Numeric(6, 3), nullable=True)
    inspector_id: Mapped[str | None] = mapped_column(ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    batch: Mapped["ManufacturingBatch | None"] = relationship(back_populates="quality_checks")
