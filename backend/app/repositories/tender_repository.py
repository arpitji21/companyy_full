from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import func, select

from app.models.tender import Tender
from app.repositories.base import BaseRepository


class TenderRepository(BaseRepository[Tender]):
    model = Tender

    def counts_by_status(self) -> dict[str, int]:
        rows = self.db.execute(select(Tender.status, func.count()).group_by(Tender.status)).all()
        return {status: count for status, count in rows}

    def total_open_bid_value(self) -> Decimal:
        return Decimal(
            self.db.scalar(
                select(func.coalesce(func.sum(Tender.bid_value), 0)).where(
                    Tender.status.in_(["draft", "submitted", "shortlisted"])
                )
            )
            or 0
        )

    def upcoming_deadlines(self, within_days: int = 14) -> int:
        cutoff = date.today() + timedelta(days=within_days)
        return (
            self.db.scalar(
                select(func.count()).where(
                    Tender.submission_deadline.is_not(None),
                    Tender.submission_deadline <= cutoff,
                    Tender.submission_deadline >= date.today(),
                )
            )
            or 0
        )
