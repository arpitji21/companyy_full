from sqlalchemy import func, select

from app.models.document import Report
from app.repositories.base import BaseRepository


class ReportRepository(BaseRepository[Report]):
    model = Report

    def total_count(self) -> int:
        return self.db.scalar(select(func.count()).select_from(Report)) or 0
