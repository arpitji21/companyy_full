from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PurchaseOrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    vendor_id: str | None
    requested_by_id: str | None
    title: str
    category: str | None
    status: str
    amount: Decimal | None
    requested_date: date | None
    approved_date: date | None
    delivery_date: date | None
    contract_end_date: date | None
    notes: str | None


class PurchaseOrderCreate(BaseModel):
    vendor_id: str | None = None
    requested_by_id: str | None = None
    title: str
    category: str | None = None
    status: str = "requested"
    amount: Decimal | None = None
    requested_date: date | None = None
    contract_end_date: date | None = None
    notes: str | None = None


class PurchaseOrderUpdate(BaseModel):
    status: str | None = None
    approved_date: date | None = None
    delivery_date: date | None = None
    contract_end_date: date | None = None
    notes: str | None = None


class ProcurementSummary(BaseModel):
    total_orders: int
    pending_approval: int
    ordered: int
    delivered: int
    total_spend: Decimal
    by_category: dict[str, Decimal]
    upcoming_contract_renewals: int  # contract_end_date within the next 30 days
