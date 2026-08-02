from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    type: str
    department_id: str | None
    category: str | None
    description: str | None
    amount: Decimal
    currency: str
    transaction_date: date
    status: str


class TransactionCreate(BaseModel):
    type: str  # revenue, expense, invoice, purchase_order
    department_id: str | None = None
    category: str | None = None
    description: str | None = None
    amount: Decimal
    currency: str = "USD"
    transaction_date: date
    status: str = "posted"


class BudgetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    department_id: str | None
    period: str
    allocated_amount: Decimal
    spent_amount: Decimal


class BudgetCreate(BaseModel):
    department_id: str | None = None
    period: str
    allocated_amount: Decimal
    spent_amount: Decimal = Decimal("0")


class FinanceSummary(BaseModel):
    total_revenue: Decimal
    total_expenses: Decimal
    net_cash_flow: Decimal
    burn_rate: Decimal  # avg monthly expenses, simple heuristic
    by_category: dict[str, Decimal]
