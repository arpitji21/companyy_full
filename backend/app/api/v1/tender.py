from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.tender import TenderCreate, TenderRead, TenderSummary, TenderUpdate
from app.services.tender_service import TenderService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/tender", tags=["Tender"])


@router.get("/summary", response_model=TenderSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return TenderService(db).summary()


@router.get("/tenders", response_model=Page[TenderRead])
def list_tenders(
    status: str | None = None,
    client_segment: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = TenderService(db).list(
        pagination.page, pagination.page_size, status=status, client_segment=client_segment
    )
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/tenders", response_model=TenderRead, status_code=201)
def create_tender(
    payload: TenderCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return TenderService(db).create(payload)


@router.get("/tenders/{tender_id}", response_model=TenderRead)
def get_tender(tender_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return TenderService(db).get(tender_id)


@router.patch("/tenders/{tender_id}", response_model=TenderRead)
def update_tender(
    tender_id: str,
    payload: TenderUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return TenderService(db).update(tender_id, payload)
