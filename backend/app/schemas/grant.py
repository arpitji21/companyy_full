from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class GrantApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    research_project_id: str | None
    title: str
    funding_body: str
    status: str
    amount_requested: Decimal | None
    amount_awarded: Decimal | None
    amount_disbursed: Decimal
    submission_date: date | None
    decision_date: date | None
    reporting_due_date: date | None
    notes: str | None


class GrantApplicationCreate(BaseModel):
    research_project_id: str | None = None
    title: str
    funding_body: str
    status: str = "draft"
    amount_requested: Decimal | None = None
    amount_awarded: Decimal | None = None
    amount_disbursed: Decimal = Decimal("0")
    submission_date: date | None = None
    decision_date: date | None = None
    reporting_due_date: date | None = None
    notes: str | None = None


class GrantApplicationUpdate(BaseModel):
    status: str | None = None
    amount_awarded: Decimal | None = None
    amount_disbursed: Decimal | None = None
    decision_date: date | None = None
    reporting_due_date: date | None = None
    notes: str | None = None


class GrantSummary(BaseModel):
    total_applications: int
    awarded: int
    under_review: int
    rejected: int
    total_awarded_amount: Decimal
    total_disbursed_amount: Decimal
    upcoming_reporting_deadlines: int  # reporting_due_date within the next 30 days
