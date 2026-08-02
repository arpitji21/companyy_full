from sqlalchemy import func, select

from app.models.clinical import ClinicalEvent, ClinicalTrial
from app.repositories.base import BaseRepository


class ClinicalTrialRepository(BaseRepository[ClinicalTrial]):
    model = ClinicalTrial

    def counts_by_status(self) -> dict[str, int]:
        rows = self.db.execute(
            select(ClinicalTrial.status, func.count()).group_by(ClinicalTrial.status)
        ).all()
        return {status: count for status, count in rows}

    def enrollment_totals(self) -> tuple[int, int]:
        target = self.db.scalar(select(func.coalesce(func.sum(ClinicalTrial.target_enrollment), 0))) or 0
        actual = self.db.scalar(select(func.coalesce(func.sum(ClinicalTrial.actual_enrollment), 0))) or 0
        return int(target), int(actual)


class ClinicalEventRepository(BaseRepository[ClinicalEvent]):
    model = ClinicalEvent

    def open_count_by_type(self, event_type: str) -> int:
        return (
            self.db.scalar(
                select(func.count()).where(
                    ClinicalEvent.event_type == event_type,
                    ClinicalEvent.status != "resolved",
                )
            )
            or 0
        )
