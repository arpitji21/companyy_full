from decimal import Decimal

from sqlalchemy import func, select

from app.models.finance import Budget, FinancialTransaction
from app.repositories.base import BaseRepository


class TransactionRepository(BaseRepository[FinancialTransaction]):
    model = FinancialTransaction

    def sum_by_type(self, type_: str) -> Decimal:
        return self.db.scalar(
            select(func.coalesce(func.sum(FinancialTransaction.amount), 0)).where(
                FinancialTransaction.type == type_
            )
        ) or Decimal("0")

    def sum_by_category(self) -> dict[str, Decimal]:
        rows = self.db.execute(
            select(FinancialTransaction.category, func.sum(FinancialTransaction.amount))
            .where(FinancialTransaction.type == "expense")
            .group_by(FinancialTransaction.category)
        ).all()
        return {(cat or "uncategorized"): amt for cat, amt in rows}


class BudgetRepository(BaseRepository[Budget]):
    model = Budget
