from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CampaignRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    channel: str
    status: str
    start_date: date | None
    end_date: date | None
    budget: Decimal | None
    impressions: int
    clicks: int
    conversions: int
    roi: float | None


class CampaignCreate(BaseModel):
    name: str
    channel: str
    status: str = "draft"
    start_date: date | None = None
    end_date: date | None = None
    budget: Decimal | None = None


class CampaignUpdate(BaseModel):
    status: str | None = None
    impressions: int | None = None
    clicks: int | None = None
    conversions: int | None = None
    roi: float | None = None


class MarketingSummary(BaseModel):
    total_campaigns: int
    active_campaigns: int
    total_impressions: int
    total_clicks: int
    total_conversions: int
    average_conversion_rate: float
