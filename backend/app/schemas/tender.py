from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class TenderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    client_name: str | None
    client_segment: str | None
    status: str
    bid_value: Decimal | None
    win_probability: Decimal | None
    submission_deadline: date | None
    outcome_date: date | None
    notes: str | None


class TenderCreate(BaseModel):
    title: str
    client_name: str | None = None
    client_segment: str | None = None
    status: str = "draft"
    bid_value: Decimal | None = None
    win_probability: Decimal | None = None
    submission_deadline: date | None = None
    notes: str | None = None


class TenderUpdate(BaseModel):
    status: str | None = None
    win_probability: Decimal | None = None
    outcome_date: date | None = None
    notes: str | None = None


class TenderSummary(BaseModel):
    total_tenders: int
    open_tenders: int
    won: int
    lost: int
    win_rate: float  # won / (won + lost), %
    total_open_bid_value: Decimal
    upcoming_deadlines: int  # submission_deadline within the next 14 days
