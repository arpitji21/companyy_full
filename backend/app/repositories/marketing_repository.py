from sqlalchemy import func, select

from app.models.marketing import MarketingCampaign
from app.repositories.base import BaseRepository


class CampaignRepository(BaseRepository[MarketingCampaign]):
    model = MarketingCampaign

    def totals(self) -> dict:
        row = self.db.execute(
            select(
                func.count(),
                func.coalesce(func.sum(MarketingCampaign.impressions), 0),
                func.coalesce(func.sum(MarketingCampaign.clicks), 0),
                func.coalesce(func.sum(MarketingCampaign.conversions), 0),
            )
        ).one()
        total, impressions, clicks, conversions = row
        return {
            "total_campaigns": total,
            "total_impressions": impressions,
            "total_clicks": clicks,
            "total_conversions": conversions,
        }

    def active_count(self) -> int:
        return self.db.scalar(
            select(func.count()).where(MarketingCampaign.status == "live")
        ) or 0
