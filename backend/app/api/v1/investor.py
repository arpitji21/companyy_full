from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.investor import (
    FundingRoundCreate,
    FundingRoundRead,
    FundingRoundUpdate,
    InvestorSummary,
    InvestorUpdateCreate,
    InvestorUpdateRead,
)
from app.services.investor_service import InvestorService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/investor", tags=["Investor"])


@router.get("/summary", response_model=InvestorSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return InvestorService(db).summary()


@router.get("/rounds", response_model=Page[FundingRoundRead])
def list_rounds(
    status: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = InvestorService(db).list_rounds(pagination.page, pagination.page_size, status=status)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/rounds", response_model=FundingRoundRead, status_code=201)
def create_round(
    payload: FundingRoundCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Investor")),
):
    return InvestorService(db).create_round(payload)


@router.get("/rounds/{round_id}", response_model=FundingRoundRead)
def get_round(round_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return InvestorService(db).get_round(round_id)


@router.patch("/rounds/{round_id}", response_model=FundingRoundRead)
def update_round(
    round_id: str,
    payload: FundingRoundUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Investor")),
):
    return InvestorService(db).update_round(round_id, payload)


@router.get("/updates", response_model=Page[InvestorUpdateRead])
def list_updates(
    update_type: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = InvestorService(db).list_updates(
        pagination.page, pagination.page_size, update_type=update_type
    )
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/updates", response_model=InvestorUpdateRead, status_code=201)
def create_update(
    payload: InvestorUpdateCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Investor")),
):
    return InvestorService(db).create_update(payload)
