from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import func, select

from app.models.procurement import PurchaseOrder
from app.repositories.base import BaseRepository


class ProcurementRepository(BaseRepository[PurchaseOrder]):
    model = PurchaseOrder

    def counts_by_status(self) -> dict[str, int]:
        rows = self.db.execute(
            select(PurchaseOrder.status, func.count()).group_by(PurchaseOrder.status)
        ).all()
        return {status: count for status, count in rows}

    def total_spend(self) -> Decimal:
        return Decimal(self.db.scalar(select(func.coalesce(func.sum(PurchaseOrder.amount), 0))) or 0)

    def spend_by_category(self) -> dict[str, Decimal]:
        rows = self.db.execute(
            select(PurchaseOrder.category, func.coalesce(func.sum(PurchaseOrder.amount), 0)).group_by(
                PurchaseOrder.category
            )
        ).all()
        return {(category or "Uncategorized"): Decimal(total) for category, total in rows}

    def upcoming_contract_renewals(self, within_days: int = 30) -> int:
        cutoff = date.today() + timedelta(days=within_days)
        return (
            self.db.scalar(
                select(func.count()).where(
                    PurchaseOrder.contract_end_date.is_not(None),
                    PurchaseOrder.contract_end_date <= cutoff,
                    PurchaseOrder.contract_end_date >= date.today(),
                )
            )
            or 0
        )
