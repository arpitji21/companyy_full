from app.core.exceptions import NotFoundError
from app.models.sales import Customer, SalesPipeline
from app.repositories.sales_repository import CustomerRepository, DealRepository
from app.schemas.sales import CustomerCreate, DealCreate, DealUpdate, SalesSummary


class SalesService:
    def __init__(self, db):
        self.db = db
        self.customers = CustomerRepository(db)
        self.deals = DealRepository(db)

    # --- Customers ---
    def list_customers(self, page: int, page_size: int):
        return self.customers.list(page=page, page_size=page_size)

    def create_customer(self, data: CustomerCreate) -> Customer:
        return self.customers.create(Customer(**data.model_dump()))

    # --- Deals / pipeline ---
    def list_deals(self, page: int, page_size: int, stage: str | None = None):
        return self.deals.list(page=page, page_size=page_size, stage=stage)

    def create_deal(self, data: DealCreate) -> SalesPipeline:
        return self.deals.create(SalesPipeline(**data.model_dump()))

    def update_deal(self, deal_id: str, data: DealUpdate) -> SalesPipeline:
        deal = self.deals.get(deal_id)
        if not deal:
            raise NotFoundError("Deal not found.")
        return self.deals.update(deal, data.model_dump(exclude_unset=True))

    def summary(self) -> SalesSummary:
        by_stage = self.deals.count_by_stage()
        open_deals = sum(count for stage, count in by_stage.items() if stage not in ("won", "lost"))
        return SalesSummary(
            total_pipeline_value=self.deals.open_pipeline_value(),
            weighted_forecast=self.deals.weighted_forecast(),
            open_deals=open_deals,
            won_deals=by_stage.get("won", 0),
            lost_deals=by_stage.get("lost", 0),
            by_stage=by_stage,
        )
