from datetime import datetime, timezone

from sqlalchemy import func, select

from app.models.customer_support import SupportTicket
from app.models.sales import Customer
from app.repositories.base import BaseRepository


class SupportTicketRepository(BaseRepository[SupportTicket]):
    model = SupportTicket

    def counts_by_status(self) -> dict[str, int]:
        rows = self.db.execute(
            select(SupportTicket.status, func.count()).group_by(SupportTicket.status)
        ).all()
        return {status: count for status, count in rows}

    def breached_sla_count(self) -> int:
        now = datetime.now(timezone.utc)
        return (
            self.db.scalar(
                select(func.count()).where(
                    SupportTicket.status.in_(["open", "pending", "escalated"]),
                    SupportTicket.sla_due_at.is_not(None),
                    SupportTicket.sla_due_at < now,
                )
            )
            or 0
        )

    def average_csat(self) -> float | None:
        avg = self.db.scalar(select(func.avg(SupportTicket.csat_score)))
        return float(avg) if avg is not None else None

    def at_risk_customer_count(self) -> int:
        return self.db.scalar(select(func.count()).where(Customer.churn_risk == "high")) or 0
