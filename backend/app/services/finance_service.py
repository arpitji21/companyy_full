from decimal import Decimal

from app.core.exceptions import NotFoundError
from app.models.finance import Budget, FinancialTransaction
from app.repositories.finance_repository import BudgetRepository, TransactionRepository
from app.schemas.finance import BudgetCreate, FinanceSummary, TransactionCreate


class FinanceService:
    def __init__(self, db):
        self.db = db
        self.transactions = TransactionRepository(db)
        self.budgets = BudgetRepository(db)

    # --- Transactions ---
    def list_transactions(self, page: int, page_size: int, type_: str | None = None, department_id: str | None = None):
        return self.transactions.list(page=page, page_size=page_size, type=type_, department_id=department_id)

    def create_transaction(self, data: TransactionCreate) -> FinancialTransaction:
        return self.transactions.create(FinancialTransaction(**data.model_dump()))

    # --- Budgets ---
    def list_budgets(self, page: int, page_size: int, department_id: str | None = None):
        return self.budgets.list(page=page, page_size=page_size, department_id=department_id)

    def create_budget(self, data: BudgetCreate) -> Budget:
        return self.budgets.create(Budget(**data.model_dump()))

    def get_budget(self, budget_id: str) -> Budget:
        budget = self.budgets.get(budget_id)
        if not budget:
            raise NotFoundError("Budget not found.")
        return budget

    # --- Summary (feeds Finance dashboard + CEO dashboard) ---
    def summary(self) -> FinanceSummary:
        revenue = self.transactions.sum_by_type("revenue")
        expenses = self.transactions.sum_by_type("expense")
        by_category = self.transactions.sum_by_category()

        # NOTE: true monthly burn rate needs a month-bucketed rollup query.
        # Until that's built, we surface total expenses as a stand-in so the
        # field is never fake/misleading data — just clearly a running total.
        burn_rate = expenses

        return FinanceSummary(
            total_revenue=revenue,
            total_expenses=expenses,
            net_cash_flow=revenue - expenses,
            burn_rate=burn_rate,
            by_category=by_category,
        )
