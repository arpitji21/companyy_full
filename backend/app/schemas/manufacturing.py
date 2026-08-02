from datetime import date

from pydantic import BaseModel, ConfigDict


class BatchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    batch_number: str
    product_name: str
    line: str | None
    quantity_produced: int
    yield_rate: float | None
    status: str
    started_at: date | None
    completed_at: date | None


class BatchCreate(BaseModel):
    batch_number: str
    product_name: str
    line: str | None = None
    quantity_produced: int = 0
    status: str = "in_progress"
    started_at: date | None = None


class BatchUpdate(BaseModel):
    quantity_produced: int | None = None
    yield_rate: float | None = None
    status: str | None = None
    completed_at: date | None = None


class QualityCheckRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    batch_id: str | None
    check_type: str
    result: str
    defect_rate: float | None
    inspector_id: str | None
    notes: str | None


class QualityCheckCreate(BaseModel):
    batch_id: str | None = None
    check_type: str
    result: str = "pending"
    defect_rate: float | None = None
    inspector_id: str | None = None
    notes: str | None = None


class ManufacturingSummary(BaseModel):
    total_batches: int
    in_progress: int
    completed: int
    average_yield_rate: float
    total_units_produced: int


class QualityMetrics(BaseModel):
    total_checks: int
    pass_count: int
    fail_count: int
    pending_count: int
    pass_rate: float
