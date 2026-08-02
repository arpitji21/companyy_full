from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.marketing import CampaignCreate, CampaignRead, CampaignUpdate, MarketingSummary
from app.services.marketing_service import MarketingService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/marketing", tags=["Marketing"])


@router.get("/summary", response_model=MarketingSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return MarketingService(db).summary()


@router.get("/campaigns", response_model=Page[CampaignRead])
def list_campaigns(
    channel: str | None = None,
    status: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = MarketingService(db).list(pagination.page, pagination.page_size, channel, status)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/campaigns", response_model=CampaignRead, status_code=201)
def create_campaign(
    payload: CampaignCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Marketing")),
):
    return MarketingService(db).create(payload)


@router.patch("/campaigns/{campaign_id}", response_model=CampaignRead)
def update_campaign(
    campaign_id: str,
    payload: CampaignUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Marketing")),
):
    return MarketingService(db).update(campaign_id, payload)
