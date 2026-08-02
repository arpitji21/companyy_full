from datetime import date

from pydantic import BaseModel, ConfigDict


class ClinicalEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    trial_id: str | None
    event_type: str
    severity: str
    status: str
    reported_date: date
    description: str | None


class ClinicalEventCreate(BaseModel):
    trial_id: str | None = None
    event_type: str
    severity: str = "mild"
    status: str = "open"
    reported_date: date
    description: str | None = None


class ClinicalTrialRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    lead_employee_id: str | None
    title: str
    phase: str
    status: str
    site: str | None
    target_enrollment: int | None
    actual_enrollment: int
    start_date: date | None
    end_date: date | None


class ClinicalTrialCreate(BaseModel):
    lead_employee_id: str | None = None
    title: str
    phase: str
    status: str = "planning"
    site: str | None = None
    target_enrollment: int | None = None
    actual_enrollment: int = 0
    start_date: date | None = None
    end_date: date | None = None


class ClinicalTrialUpdate(BaseModel):
    status: str | None = None
    actual_enrollment: int | None = None
    site: str | None = None
    end_date: date | None = None


class ClinicalSummary(BaseModel):
    total_trials: int
    active_trials: int
    completed_trials: int
    total_target_enrollment: int
    total_actual_enrollment: int
    enrollment_rate: float  # actual / target, %
    open_adverse_events: int
    open_protocol_deviations: int
