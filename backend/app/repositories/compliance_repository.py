from sqlalchemy import func, select

from app.models.compliance import ComplianceRecord
from app.repositories.base import BaseRepository


class ComplianceRepository(BaseRepository[ComplianceRecord]):
    model = ComplianceRecord

    def counts_by_status(self) -> dict[str, int]:
        rows = self.db.execute(
            select(ComplianceRecord.status, func.count()).group_by(ComplianceRecord.status)
        ).all()
        return {status: count for status, count in rows}
