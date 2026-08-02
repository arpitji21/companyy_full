from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class FundingRoundRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    round_name: str
    status: str
    amount_raised: Decimal | None
    pre_money_valuation: Decimal | None
    post_money_valuation: Decimal | None
    lead_investor: str | None
    close_date: date | None
    notes: str | None


class FundingRoundCreate(BaseModel):
    round_name: str
    status: str = "planned"
    amount_raised: Decimal | None = None
    pre_money_valuation: Decimal | None = None
    post_money_valuation: Decimal | None = None
    lead_investor: str | None = None
    close_date: date | None = None
    notes: str | None = None


class FundingRoundUpdate(BaseModel):
    status: str | None = None
    amount_raised: Decimal | None = None
    post_money_valuation: Decimal | None = None
    close_date: date | None = None
    notes: str | None = None


class InvestorUpdateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    update_type: str
    sent_date: date | None
    next_report_due_date: date | None
    summary: str | None


class InvestorUpdateCreate(BaseModel):
    title: str
    update_type: str = "investor_update"
    sent_date: date | None = None
    next_report_due_date: date | None = None
    summary: str | None = None


class InvestorSummary(BaseModel):
    total_raised: Decimal
    latest_post_money_valuation: Decimal | None
    open_rounds: int
    closed_rounds: int
    next_report_due_date: date | None
    updates_last_90_days: int
