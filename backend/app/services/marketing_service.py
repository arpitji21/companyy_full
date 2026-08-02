from app.core.exceptions import NotFoundError
from app.models.marketing import MarketingCampaign
from app.repositories.marketing_repository import CampaignRepository
from app.schemas.marketing import CampaignCreate, CampaignUpdate, MarketingSummary


class MarketingService:
    def __init__(self, db):
        self.db = db
        self.repo = CampaignRepository(db)

    def list(self, page: int, page_size: int, channel: str | None = None, status: str | None = None):
        return self.repo.list(page=page, page_size=page_size, channel=channel, status=status)

    def create(self, data: CampaignCreate) -> MarketingCampaign:
        return self.repo.create(MarketingCampaign(**data.model_dump()))

    def update(self, campaign_id: str, data: CampaignUpdate) -> MarketingCampaign:
        campaign = self.repo.get(campaign_id)
        if not campaign:
            raise NotFoundError("Campaign not found.")
        return self.repo.update(campaign, data.model_dump(exclude_unset=True))

    def summary(self) -> MarketingSummary:
        totals = self.repo.totals()
        active = self.repo.active_count()
        clicks = totals["total_clicks"]
        conversions = totals["total_conversions"]
        conversion_rate = (conversions / clicks * 100) if clicks else 0.0
        return MarketingSummary(
            total_campaigns=totals["total_campaigns"],
            active_campaigns=active,
            total_impressions=totals["total_impressions"],
            total_clicks=clicks,
            total_conversions=conversions,
            average_conversion_rate=round(conversion_rate, 2),
        )
