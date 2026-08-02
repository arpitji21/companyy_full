from app.core.exceptions import NotFoundError
from app.models.procurement import PurchaseOrder
from app.repositories.procurement_repository import ProcurementRepository
from app.schemas.procurement import ProcurementSummary, PurchaseOrderCreate, PurchaseOrderUpdate


class ProcurementService:
    def __init__(self, db):
        self.db = db
        self.repo = ProcurementRepository(db)

    def list(self, page: int, page_size: int, status: str | None = None, category: str | None = None):
        return self.repo.list(page=page, page_size=page_size, status=status, category=category)

    def get(self, order_id: str) -> PurchaseOrder:
        order = self.repo.get(order_id)
        if not order:
            raise NotFoundError("Purchase order not found.")
        return order

    def create(self, data: PurchaseOrderCreate) -> PurchaseOrder:
        return self.repo.create(PurchaseOrder(**data.model_dump()))

    def update(self, order_id: str, data: PurchaseOrderUpdate) -> PurchaseOrder:
        order = self.get(order_id)
        return self.repo.update(order, data.model_dump(exclude_unset=True))

    def summary(self) -> ProcurementSummary:
        by_status = self.repo.counts_by_status()
        return ProcurementSummary(
            total_orders=sum(by_status.values()),
            pending_approval=by_status.get("requested", 0),
            ordered=by_status.get("ordered", 0),
            delivered=by_status.get("delivered", 0),
            total_spend=self.repo.total_spend(),
            by_category=self.repo.spend_by_category(),
            upcoming_contract_renewals=self.repo.upcoming_contract_renewals(),
        )
