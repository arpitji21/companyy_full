from decimal import Decimal

from sqlalchemy import func, select

from app.models.sales import Customer, SalesPipeline
from app.repositories.base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    model = Customer


class DealRepository(BaseRepository[SalesPipeline]):
    model = SalesPipeline

    def count_by_stage(self) -> dict[str, int]:
        rows = self.db.execute(
            select(SalesPipeline.stage, func.count()).group_by(SalesPipeline.stage)
        ).all()
        return {stage: count for stage, count in rows}

    def open_pipeline_value(self) -> Decimal:
        return self.db.scalar(
            select(func.coalesce(func.sum(SalesPipeline.amount), 0)).where(
                SalesPipeline.stage.notin_(["won", "lost"])
            )
        ) or Decimal("0")

    def weighted_forecast(self) -> Decimal:
        rows = self.db.execute(
            select(SalesPipeline.amount, SalesPipeline.probability).where(
                SalesPipeline.stage.notin_(["won", "lost"])
            )
        ).all()
        return sum((amount * Decimal(probability) / Decimal(100) for amount, probability in rows), Decimal("0"))
