from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.patent import PatentFilingCreate, PatentFilingRead, PatentFilingUpdate, PatentSummary
from app.services.patent_service import PatentService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/patent", tags=["Patent"])


@router.get("/summary", response_model=PatentSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return PatentService(db).summary()


@router.get("/filings", response_model=Page[PatentFilingRead])
def list_filings(
    status: str | None = None,
    jurisdiction: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = PatentService(db).list(
        pagination.page, pagination.page_size, status=status, jurisdiction=jurisdiction
    )
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/filings", response_model=PatentFilingRead, status_code=201)
def create_filing(
    payload: PatentFilingCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Research")),
):
    return PatentService(db).create(payload)


@router.get("/filings/{filing_id}", response_model=PatentFilingRead)
def get_filing(filing_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return PatentService(db).get(filing_id)


@router.patch("/filings/{filing_id}", response_model=PatentFilingRead)
def update_filing(
    filing_id: str,
    payload: PatentFilingUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Research")),
):
    return PatentService(db).update(filing_id, payload)
