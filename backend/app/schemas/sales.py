from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    company: str | None
    email: EmailStr | None
    csat_score: float | None
    churn_risk: str
    owner_id: str | None


class CustomerCreate(BaseModel):
    name: str
    company: str | None = None
    email: EmailStr | None = None
    owner_id: str | None = None


class DealRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    customer_id: str | None
    owner_id: str | None
    deal_name: str
    stage: str
    amount: Decimal
    probability: int
    expected_close_date: str | None


class DealCreate(BaseModel):
    customer_id: str | None = None
    owner_id: str | None = None
    deal_name: str
    stage: str = "lead"
    amount: Decimal
    probability: int = 10
    expected_close_date: str | None = None


class DealUpdate(BaseModel):
    stage: str | None = None
    amount: Decimal | None = None
    probability: int | None = None
    expected_close_date: str | None = None


class SalesSummary(BaseModel):
    total_pipeline_value: Decimal
    weighted_forecast: Decimal
    open_deals: int
    won_deals: int
    lost_deals: int
    by_stage: dict[str, int]
