from app.core.exceptions import NotFoundError
from app.models.grant import GrantApplication
from app.repositories.grant_repository import GrantRepository
from app.schemas.grant import GrantApplicationCreate, GrantApplicationUpdate, GrantSummary


class GrantService:
    def __init__(self, db):
        self.db = db
        self.repo = GrantRepository(db)

    def list(self, page: int, page_size: int, status: str | None = None, funding_body: str | None = None):
        return self.repo.list(page=page, page_size=page_size, status=status, funding_body=funding_body)

    def get(self, application_id: str) -> GrantApplication:
        application = self.repo.get(application_id)
        if not application:
            raise NotFoundError("Grant application not found.")
        return application

    def create(self, data: GrantApplicationCreate) -> GrantApplication:
        return self.repo.create(GrantApplication(**data.model_dump()))

    def update(self, application_id: str, data: GrantApplicationUpdate) -> GrantApplication:
        application = self.get(application_id)
        return self.repo.update(application, data.model_dump(exclude_unset=True))

    def summary(self) -> GrantSummary:
        by_status = self.repo.counts_by_status()
        awarded_total, disbursed_total = self.repo.totals()
        return GrantSummary(
            total_applications=sum(by_status.values()),
            awarded=by_status.get("awarded", 0),
            under_review=by_status.get("under_review", 0) + by_status.get("submitted", 0),
            rejected=by_status.get("rejected", 0),
            total_awarded_amount=awarded_total,
            total_disbursed_amount=disbursed_total,
            upcoming_reporting_deadlines=self.repo.upcoming_reporting_deadlines(),
        )
