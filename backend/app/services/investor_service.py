from app.core.exceptions import NotFoundError
from app.models.investor import FundingRound, InvestorUpdate
from app.repositories.investor_repository import FundingRoundRepository, InvestorUpdateRepository
from app.schemas.investor import (
    FundingRoundCreate,
    FundingRoundUpdate,
    InvestorSummary,
    InvestorUpdateCreate,
)


class InvestorService:
    def __init__(self, db):
        self.db = db
        self.rounds = FundingRoundRepository(db)
        self.updates = InvestorUpdateRepository(db)

    def list_rounds(self, page: int, page_size: int, status: str | None = None):
        return self.rounds.list(page=page, page_size=page_size, status=status)

    def get_round(self, round_id: str) -> FundingRound:
        round_ = self.rounds.get(round_id)
        if not round_:
            raise NotFoundError("Funding round not found.")
        return round_

    def create_round(self, data: FundingRoundCreate) -> FundingRound:
        return self.rounds.create(FundingRound(**data.model_dump()))

    def update_round(self, round_id: str, data: FundingRoundUpdate) -> FundingRound:
        round_ = self.get_round(round_id)
        return self.rounds.update(round_, data.model_dump(exclude_unset=True))

    def list_updates(self, page: int, page_size: int, update_type: str | None = None):
        return self.updates.list(page=page, page_size=page_size, update_type=update_type)

    def create_update(self, data: InvestorUpdateCreate) -> InvestorUpdate:
        return self.updates.create(InvestorUpdate(**data.model_dump()))

    def summary(self) -> InvestorSummary:
        by_status = self.rounds.counts_by_status()
        return InvestorSummary(
            total_raised=self.rounds.total_raised(),
            latest_post_money_valuation=self.rounds.latest_post_money_valuation(),
            open_rounds=by_status.get("planned", 0) + by_status.get("in_progress", 0),
            closed_rounds=by_status.get("closed", 0),
            next_report_due_date=self.updates.next_report_due_date(),
            updates_last_90_days=self.updates.count_since(90),
        )
