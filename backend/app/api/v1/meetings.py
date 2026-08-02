from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.meeting import MeetingCreate, MeetingRead
from app.services.meeting_service import MeetingService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/meetings", tags=["Meetings"])


@router.get("", response_model=Page[MeetingRead])
def list_meetings(
    department_id: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = MeetingService(db).list(pagination.page, pagination.page_size, department_id)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.get("/upcoming", response_model=list[MeetingRead])
def upcoming_meetings(limit: int = 10, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return MeetingService(db).upcoming(limit)


@router.post("", response_model=MeetingRead, status_code=201)
def create_meeting(payload: MeetingCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return MeetingService(db).create(payload)
