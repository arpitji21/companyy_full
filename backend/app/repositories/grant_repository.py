from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import func, select

from app.models.grant import GrantApplication
from app.repositories.base import BaseRepository


class GrantRepository(BaseRepository[GrantApplication]):
    model = GrantApplication

    def counts_by_status(self) -> dict[str, int]:
        rows = self.db.execute(
            select(GrantApplication.status, func.count()).group_by(GrantApplication.status)
        ).all()
        return {status: count for status, count in rows}

    def totals(self) -> tuple[Decimal, Decimal]:
        awarded_total = self.db.scalar(select(func.coalesce(func.sum(GrantApplication.amount_awarded), 0))) or 0
        disbursed_total = self.db.scalar(select(func.coalesce(func.sum(GrantApplication.amount_disbursed), 0))) or 0
        return Decimal(awarded_total), Decimal(disbursed_total)

    def upcoming_reporting_deadlines(self, within_days: int = 30) -> int:
        cutoff = date.today() + timedelta(days=within_days)
        return (
            self.db.scalar(
                select(func.count()).where(
                    GrantApplication.reporting_due_date.is_not(None),
                    GrantApplication.reporting_due_date <= cutoff,
                    GrantApplication.reporting_due_date >= date.today(),
                )
            )
            or 0
        )
