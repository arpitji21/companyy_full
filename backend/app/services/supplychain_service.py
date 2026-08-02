from app.core.exceptions import NotFoundError
from app.models.vendor import Inventory, Vendor
from app.repositories.supplychain_repository import InventoryRepository, VendorRepository
from app.schemas.supplychain import (
    InventoryItemCreate,
    InventoryItemUpdate,
    SupplyChainSummary,
    VendorCreate,
)


class SupplyChainService:
    def __init__(self, db):
        self.db = db
        self.vendors = VendorRepository(db)
        self.inventory = InventoryRepository(db)

    def list_vendors(self, page: int, page_size: int):
        return self.vendors.list(page=page, page_size=page_size)

    def create_vendor(self, data: VendorCreate) -> Vendor:
        return self.vendors.create(Vendor(**data.model_dump()))

    def list_inventory(self, page: int, page_size: int):
        return self.inventory.list(page=page, page_size=page_size)

    def create_inventory_item(self, data: InventoryItemCreate) -> Inventory:
        return self.inventory.create(Inventory(**data.model_dump()))

    def update_inventory_item(self, item_id: str, data: InventoryItemUpdate) -> Inventory:
        item = self.inventory.get(item_id)
        if not item:
            raise NotFoundError("Inventory item not found.")
        return self.inventory.update(item, data.model_dump(exclude_unset=True))

    def summary(self) -> SupplyChainSummary:
        _, vendor_total = self.vendors.list(page=1, page_size=1)
        _, sku_total = self.inventory.list(page=1, page_size=1)
        return SupplyChainSummary(
            total_vendors=vendor_total,
            total_sku_count=sku_total,
            items_below_reorder_level=self.inventory.below_reorder_count(),
        )
