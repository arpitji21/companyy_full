from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.compliance import ComplianceRecordCreate, ComplianceRecordRead, ComplianceSummary
from app.services.compliance_service import ComplianceService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/regulatory", tags=["Regulatory"])

# Regulatory submissions (FDA, CDSCO, ISO, MDR, ...) are the same underlying
# `compliance_records` table as /api/compliance, just scoped by `framework`.
# Kept as its own router/URL because the frontend treats it as a distinct
# department, but there's deliberately no separate table to avoid
# duplicating compliance data in two places.


@router.get("/summary", response_model=ComplianceSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ComplianceService(db).summary()


@router.get("/submissions", response_model=Page[ComplianceRecordRead])
def list_submissions(
    framework: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = ComplianceService(db).list(pagination.page, pagination.page_size, framework=framework)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/submissions", response_model=ComplianceRecordRead, status_code=201)
def create_submission(
    payload: ComplianceRecordCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Regulatory")),
):
    return ComplianceService(db).create(payload)
