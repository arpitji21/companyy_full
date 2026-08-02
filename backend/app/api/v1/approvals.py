from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.approval import ApprovalCreate, ApprovalDecision, ApprovalRead
from app.schemas.common import Page
from app.services.approval_service import ApprovalService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.get("", response_model=Page[ApprovalRead])
def list_approvals(
    status: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = ApprovalService(db).list(pagination.page, pagination.page_size, status)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("", response_model=ApprovalRead, status_code=201)
def create_approval(payload: ApprovalCreate, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    return ApprovalService(db).create(payload, requested_by=user.id)


@router.post("/{approval_id}/decision", response_model=ApprovalRead)
def decide_approval(
    approval_id: str,
    payload: ApprovalDecision,
    db: Session = Depends(get_db),
    user=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return ApprovalService(db).decide(approval_id, payload, approver_id=user.id)
