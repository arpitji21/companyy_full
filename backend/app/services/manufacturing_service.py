from app.core.exceptions import NotFoundError
from app.models.manufacturing import ManufacturingBatch
from app.repositories.manufacturing_repository import BatchRepository
from app.schemas.manufacturing import BatchCreate, BatchUpdate, ManufacturingSummary


class ManufacturingService:
    def __init__(self, db):
        self.db = db
        self.repo = BatchRepository(db)

    def list(self, page: int, page_size: int, status: str | None = None):
        return self.repo.list(page=page, page_size=page_size, status=status)

    def create(self, data: BatchCreate) -> ManufacturingBatch:
        return self.repo.create(ManufacturingBatch(**data.model_dump()))

    def update(self, batch_id: str, data: BatchUpdate) -> ManufacturingBatch:
        batch = self.repo.get(batch_id)
        if not batch:
            raise NotFoundError("Manufacturing batch not found.")
        return self.repo.update(batch, data.model_dump(exclude_unset=True))

    def summary(self) -> ManufacturingSummary:
        by_status = self.repo.counts_by_status()
        return ManufacturingSummary(
            total_batches=sum(by_status.values()),
            in_progress=by_status.get("in_progress", 0),
            completed=by_status.get("completed", 0),
            average_yield_rate=round(float(self.repo.average_yield()), 2),
            total_units_produced=self.repo.total_units(),
        )
