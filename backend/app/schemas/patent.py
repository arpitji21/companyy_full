from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PatentFilingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    research_project_id: str | None
    title: str
    jurisdiction: str
    status: str
    application_number: str | None
    filing_date: date | None
    grant_date: date | None
    renewal_date: date | None
    estimated_value: Decimal | None
    notes: str | None


class PatentFilingCreate(BaseModel):
    research_project_id: str | None = None
    title: str
    jurisdiction: str
    status: str = "draft"
    application_number: str | None = None
    filing_date: date | None = None
    grant_date: date | None = None
    renewal_date: date | None = None
    estimated_value: Decimal | None = None
    notes: str | None = None


class PatentFilingUpdate(BaseModel):
    status: str | None = None
    application_number: str | None = None
    grant_date: date | None = None
    renewal_date: date | None = None
    estimated_value: Decimal | None = None
    notes: str | None = None


class PatentSummary(BaseModel):
    total_filings: int
    granted: int
    pending: int
    rejected: int
    upcoming_renewals: int  # renewal_date within the next 90 days
    total_portfolio_value: Decimal
