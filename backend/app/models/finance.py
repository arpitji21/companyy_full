from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class FinancialTransaction(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "financial_transactions"

    type: Mapped[str] = mapped_column(String(20))  # revenue, expense, invoice, purchase_order
    department_id: Mapped[str | None] = mapped_column(ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    transaction_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="posted")  # draft, posted, paid, overdue


class Budget(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "budgets"

    department_id: Mapped[str | None] = mapped_column(ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    period: Mapped[str] = mapped_column(String(20))  # "2026-Q3", "2026-07"
    allocated_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    spent_amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
