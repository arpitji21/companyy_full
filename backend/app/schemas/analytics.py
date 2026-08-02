from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    department_id: str | None
    report_type: str
    period_start: str | None
    period_end: str | None
    generated_by: str | None
    s3_key: str | None


class ReportCreate(BaseModel):
    title: str
    department_id: str | None = None
    report_type: str = "custom"  # monthly, board, compliance, custom
    period_start: str | None = None
    period_end: str | None = None


class DepartmentSnapshot(BaseModel):
    """One tile per source department in the cross-department view."""

    department: str
    headline_metric: str
    headline_value: str
    secondary_metric: str
    secondary_value: str


class AnalyticsSummary(BaseModel):
    total_revenue: Decimal
    total_expenses: Decimal
    net_cash_flow: Decimal
    open_pipeline_value: Decimal
    manufacturing_yield_rate: float
    compliance_score: float
    total_reports: int
    snapshots: list[DepartmentSnapshot]
