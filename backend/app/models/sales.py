from __future__ import annotations

from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class Customer(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(String(255))
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    csat_score: Mapped[float | None] = mapped_column(Numeric(3, 2), nullable=True)
    churn_risk: Mapped[str] = mapped_column(String(20), default="low")  # low, medium, high
    owner_id: Mapped[str | None] = mapped_column(ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)

    deals: Mapped[list["SalesPipeline"]] = relationship(back_populates="customer")


class SalesPipeline(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "sales_pipeline"

    customer_id: Mapped[str | None] = mapped_column(ForeignKey("customers.id", ondelete="SET NULL"), nullable=True)
    owner_id: Mapped[str | None] = mapped_column(ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)

    deal_name: Mapped[str] = mapped_column(String(255))
    stage: Mapped[str] = mapped_column(String(30), default="lead")  # lead, qualified, proposal, negotiation, won, lost
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    probability: Mapped[int] = mapped_column(Integer, default=10)  # 0-100
    expected_close_date: Mapped[str | None] = mapped_column(String(20), nullable=True)

    customer: Mapped["Customer | None"] = relationship(back_populates="deals")
