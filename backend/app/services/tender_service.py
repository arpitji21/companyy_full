from app.core.exceptions import NotFoundError
from app.models.tender import Tender
from app.repositories.tender_repository import TenderRepository
from app.schemas.tender import TenderCreate, TenderSummary, TenderUpdate


class TenderService:
    def __init__(self, db):
        self.db = db
        self.repo = TenderRepository(db)

    def list(self, page: int, page_size: int, status: str | None = None, client_segment: str | None = None):
        return self.repo.list(page=page, page_size=page_size, status=status, client_segment=client_segment)

    def get(self, tender_id: str) -> Tender:
        tender = self.repo.get(tender_id)
        if not tender:
            raise NotFoundError("Tender not found.")
        return tender

    def create(self, data: TenderCreate) -> Tender:
        return self.repo.create(Tender(**data.model_dump()))

    def update(self, tender_id: str, data: TenderUpdate) -> Tender:
        tender = self.get(tender_id)
        return self.repo.update(tender, data.model_dump(exclude_unset=True))

    def summary(self) -> TenderSummary:
        by_status = self.repo.counts_by_status()
        won = by_status.get("won", 0)
        lost = by_status.get("lost", 0)
        decided = won + lost
        return TenderSummary(
            total_tenders=sum(by_status.values()),
            open_tenders=by_status.get("draft", 0) + by_status.get("submitted", 0) + by_status.get("shortlisted", 0),
            won=won,
            lost=lost,
            win_rate=round((won / decided * 100), 1) if decided else 0.0,
            total_open_bid_value=self.repo.total_open_bid_value(),
            upcoming_deadlines=self.repo.upcoming_deadlines(),
        )
