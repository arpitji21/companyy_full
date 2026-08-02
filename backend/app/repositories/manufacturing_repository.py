from sqlalchemy import func, select

from app.models.manufacturing import ManufacturingBatch, QualityCheck
from app.repositories.base import BaseRepository


class BatchRepository(BaseRepository[ManufacturingBatch]):
    model = ManufacturingBatch

    def counts_by_status(self) -> dict[str, int]:
        rows = self.db.execute(
            select(ManufacturingBatch.status, func.count()).group_by(ManufacturingBatch.status)
        ).all()
        return {status: count for status, count in rows}

    def average_yield(self) -> float:
        return self.db.scalar(select(func.avg(ManufacturingBatch.yield_rate))) or 0.0

    def total_units(self) -> int:
        return self.db.scalar(select(func.coalesce(func.sum(ManufacturingBatch.quantity_produced), 0))) or 0


class QualityCheckRepository(BaseRepository[QualityCheck]):
    model = QualityCheck

    def counts_by_result(self) -> dict[str, int]:
        rows = self.db.execute(
            select(QualityCheck.result, func.count()).group_by(QualityCheck.result)
        ).all()
        return {result: count for result, count in rows}
