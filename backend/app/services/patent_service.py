from app.core.exceptions import NotFoundError
from app.models.patent import PatentFiling
from app.repositories.patent_repository import PatentRepository
from app.schemas.patent import PatentFilingCreate, PatentFilingUpdate, PatentSummary


class PatentService:
    def __init__(self, db):
        self.db = db
        self.repo = PatentRepository(db)

    def list(self, page: int, page_size: int, status: str | None = None, jurisdiction: str | None = None):
        return self.repo.list(page=page, page_size=page_size, status=status, jurisdiction=jurisdiction)

    def get(self, filing_id: str) -> PatentFiling:
        filing = self.repo.get(filing_id)
        if not filing:
            raise NotFoundError("Patent filing not found.")
        return filing

    def create(self, data: PatentFilingCreate) -> PatentFiling:
        return self.repo.create(PatentFiling(**data.model_dump()))

    def update(self, filing_id: str, data: PatentFilingUpdate) -> PatentFiling:
        filing = self.get(filing_id)
        return self.repo.update(filing, data.model_dump(exclude_unset=True))

    def summary(self) -> PatentSummary:
        by_status = self.repo.counts_by_status()
        return PatentSummary(
            total_filings=sum(by_status.values()),
            granted=by_status.get("granted", 0),
            pending=by_status.get("pending", 0) + by_status.get("filed", 0),
            rejected=by_status.get("rejected", 0),
            upcoming_renewals=self.repo.upcoming_renewals(),
            total_portfolio_value=self.repo.total_estimated_value(),
        )
