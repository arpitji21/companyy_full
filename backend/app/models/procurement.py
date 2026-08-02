from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class PurchaseOrder(UUIDPKMixin, TimestampMixin, Base):
    """Purchase requisition -> PO -> delivery, in one row. Distinct from
    Supply Chain's vendor/inventory view, which tracks what's on hand
    rather than what's being bought."""

    __tablename__ = "purchase_orders"

    vendor_id: Mapped[str | None] = mapped_column(ForeignKey("vendors.id", ondelete="SET NULL"), nullable=True)
    requested_by_id: Mapped[str | None] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )

    title: Mapped[str] = mapped_column(String(255))
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="requested")  # requested, approved, ordered, delivered, rejected, cancelled
    amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)

    requested_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    approved_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    delivery_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    contract_end_date: Mapped[date | None] = mapped_column(Date, nullable=True)  # for renewal reminders

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    vendor: Mapped["Vendor | None"] = relationship()  # noqa: F821
