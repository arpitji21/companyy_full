from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.manufacturing import BatchCreate, BatchRead, BatchUpdate, ManufacturingSummary
from app.services.manufacturing_service import ManufacturingService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/manufacturing", tags=["Manufacturing"])


@router.get("/summary", response_model=ManufacturingSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ManufacturingService(db).summary()


@router.get("/batches", response_model=Page[BatchRead])
def list_batches(
    status: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = ManufacturingService(db).list(pagination.page, pagination.page_size, status)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/batches", response_model=BatchRead, status_code=201)
def create_batch(
    payload: BatchCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return ManufacturingService(db).create(payload)


@router.patch("/batches/{batch_id}", response_model=BatchRead)
def update_batch(
    batch_id: str,
    payload: BatchUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return ManufacturingService(db).update(batch_id, payload)
