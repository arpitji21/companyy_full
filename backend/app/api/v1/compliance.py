from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.compliance import (
    ComplianceRecordCreate,
    ComplianceRecordRead,
    ComplianceRecordUpdate,
    ComplianceSummary,
)
from app.services.compliance_service import ComplianceService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/compliance", tags=["Compliance"])


@router.get("/summary", response_model=ComplianceSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ComplianceService(db).summary()


@router.get("/records", response_model=Page[ComplianceRecordRead])
def list_records(
    framework: str | None = None,
    status: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = ComplianceService(db).list(pagination.page, pagination.page_size, framework, status)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/records", response_model=ComplianceRecordRead, status_code=201)
def create_record(
    payload: ComplianceRecordCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Compliance", "Regulatory")),
):
    return ComplianceService(db).create(payload)


@router.patch("/records/{record_id}", response_model=ComplianceRecordRead)
def update_record(
    record_id: str,
    payload: ComplianceRecordUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Compliance", "Regulatory")),
):
    return ComplianceService(db).update(record_id, payload)
