from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import func, select

from app.models.investor import FundingRound, InvestorUpdate
from app.repositories.base import BaseRepository


class FundingRoundRepository(BaseRepository[FundingRound]):
    model = FundingRound

    def total_raised(self) -> Decimal:
        return Decimal(self.db.scalar(select(func.coalesce(func.sum(FundingRound.amount_raised), 0))) or 0)

    def counts_by_status(self) -> dict[str, int]:
        rows = self.db.execute(
            select(FundingRound.status, func.count()).group_by(FundingRound.status)
        ).all()
        return {status: count for status, count in rows}

    def latest_post_money_valuation(self) -> Decimal | None:
        row = self.db.scalar(
            select(FundingRound.post_money_valuation)
            .where(FundingRound.close_date.is_not(None))
            .order_by(FundingRound.close_date.desc())
            .limit(1)
        )
        return row


class InvestorUpdateRepository(BaseRepository[InvestorUpdate]):
    model = InvestorUpdate

    def next_report_due_date(self) -> date | None:
        return self.db.scalar(
            select(InvestorUpdate.next_report_due_date)
            .where(InvestorUpdate.next_report_due_date.is_not(None))
            .order_by(InvestorUpdate.next_report_due_date.asc())
            .limit(1)
        )

    def count_since(self, days: int = 90) -> int:
        cutoff = date.today() - timedelta(days=days)
        return (
            self.db.scalar(
                select(func.count()).where(
                    InvestorUpdate.sent_date.is_not(None), InvestorUpdate.sent_date >= cutoff
                )
            )
            or 0
        )
