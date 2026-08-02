from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.grant import GrantApplicationCreate, GrantApplicationRead, GrantApplicationUpdate, GrantSummary
from app.services.grant_service import GrantService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/grant", tags=["Grant"])


@router.get("/summary", response_model=GrantSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return GrantService(db).summary()


@router.get("/applications", response_model=Page[GrantApplicationRead])
def list_applications(
    status: str | None = None,
    funding_body: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = GrantService(db).list(
        pagination.page, pagination.page_size, status=status, funding_body=funding_body
    )
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/applications", response_model=GrantApplicationRead, status_code=201)
def create_application(
    payload: GrantApplicationCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Research")),
):
    return GrantService(db).create(payload)


@router.get("/applications/{application_id}", response_model=GrantApplicationRead)
def get_application(application_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return GrantService(db).get(application_id)


@router.patch("/applications/{application_id}", response_model=GrantApplicationRead)
def update_application(
    application_id: str,
    payload: GrantApplicationUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Research")),
):
    return GrantService(db).update(application_id, payload)
