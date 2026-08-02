from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import func, select

from app.models.patent import PatentFiling
from app.repositories.base import BaseRepository


class PatentRepository(BaseRepository[PatentFiling]):
    model = PatentFiling

    def counts_by_status(self) -> dict[str, int]:
        rows = self.db.execute(
            select(PatentFiling.status, func.count()).group_by(PatentFiling.status)
        ).all()
        return {status: count for status, count in rows}

    def total_estimated_value(self) -> Decimal:
        total = self.db.scalar(select(func.coalesce(func.sum(PatentFiling.estimated_value), 0)))
        return Decimal(total or 0)

    def upcoming_renewals(self, within_days: int = 90) -> int:
        cutoff = date.today() + timedelta(days=within_days)
        return (
            self.db.scalar(
                select(func.count()).where(
                    PatentFiling.renewal_date.is_not(None),
                    PatentFiling.renewal_date <= cutoff,
                    PatentFiling.renewal_date >= date.today(),
                )
            )
            or 0
        )
