from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.manufacturing import QualityCheckCreate, QualityCheckRead, QualityMetrics
from app.services.quality_service import QualityService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/quality", tags=["Quality"])


@router.get("/metrics", response_model=QualityMetrics)
def get_metrics(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return QualityService(db).metrics()


@router.get("/checks", response_model=Page[QualityCheckRead])
def list_checks(
    check_type: str | None = None,
    result: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = QualityService(db).list(pagination.page, pagination.page_size, check_type, result)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/checks", response_model=QualityCheckRead, status_code=201)
def create_check(
    payload: QualityCheckCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Quality")),
):
    return QualityService(db).create(payload)
