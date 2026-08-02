from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.notification import NotificationCreate, NotificationRead
from app.services.notification_service import NotificationService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=Page[NotificationRead])
def list_my_notifications(
    unread_only: bool = False,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user),
):
    items, total = NotificationService(db).list_for_user(user.id, pagination.page, pagination.page_size, unread_only)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.get("/unread-count")
def unread_count(db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    return {"unread_count": NotificationService(db).unread_count(user.id)}


@router.post("", response_model=NotificationRead, status_code=201)
def create_notification(
    payload: NotificationCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin")),
):
    # System/admin-triggered for now — Phase 5 adds the WebSocket push layer
    # and workflow-driven auto-creation (task assigned, approval needed, etc).
    return NotificationService(db).create(payload)


@router.post("/{notification_id}/read", response_model=NotificationRead)
def mark_read(notification_id: str, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    return NotificationService(db).mark_read(notification_id, user.id)
