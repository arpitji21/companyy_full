from datetime import date

from pydantic import BaseModel, ConfigDict


class ComplianceRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    framework: str
    title: str
    status: str
    submission_date: date | None
    expiry_date: date | None
    certificate_number: str | None
    notes: str | None


class ComplianceRecordCreate(BaseModel):
    framework: str
    title: str
    status: str = "in_progress"
    submission_date: date | None = None
    expiry_date: date | None = None
    certificate_number: str | None = None
    notes: str | None = None


class ComplianceRecordUpdate(BaseModel):
    status: str | None = None
    expiry_date: date | None = None
    certificate_number: str | None = None
    notes: str | None = None


class ComplianceSummary(BaseModel):
    total_records: int
    approved: int
    expired: int
    in_progress: int
    compliance_score: float  # % of records approved & not expired
