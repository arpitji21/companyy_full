from sqlalchemy import func, select

from app.models.vendor import Inventory, Vendor
from app.repositories.base import BaseRepository


class VendorRepository(BaseRepository[Vendor]):
    model = Vendor


class InventoryRepository(BaseRepository[Inventory]):
    model = Inventory

    def below_reorder_count(self) -> int:
        return self.db.scalar(
            select(func.count()).where(Inventory.quantity_on_hand < Inventory.reorder_level)
        ) or 0
