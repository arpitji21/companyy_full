from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class VendorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    category: str | None
    contact_email: str | None
    contact_phone: str | None
    on_time_delivery_rate: float | None
    status: str


class VendorCreate(BaseModel):
    name: str
    category: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None


class InventoryItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    sku: str
    name: str
    category: str | None
    quantity_on_hand: int
    reorder_level: int
    unit_cost: Decimal | None
    warehouse_location: str | None
    vendor_id: str | None


class InventoryItemCreate(BaseModel):
    sku: str
    name: str
    category: str | None = None
    quantity_on_hand: int = 0
    reorder_level: int = 0
    unit_cost: Decimal | None = None
    warehouse_location: str | None = None
    vendor_id: str | None = None


class InventoryItemUpdate(BaseModel):
    quantity_on_hand: int | None = None
    reorder_level: int | None = None
    warehouse_location: str | None = None


class SupplyChainSummary(BaseModel):
    total_vendors: int
    total_sku_count: int
    items_below_reorder_level: int
