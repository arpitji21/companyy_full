from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.clinical import (
    ClinicalEventCreate,
    ClinicalEventRead,
    ClinicalSummary,
    ClinicalTrialCreate,
    ClinicalTrialRead,
    ClinicalTrialUpdate,
)
from app.schemas.common import Page
from app.services.clinical_service import ClinicalService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/clinical", tags=["Clinical"])


@router.get("/summary", response_model=ClinicalSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ClinicalService(db).summary()


@router.get("/trials", response_model=Page[ClinicalTrialRead])
def list_trials(
    status: str | None = None,
    phase: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = ClinicalService(db).list_trials(pagination.page, pagination.page_size, status=status, phase=phase)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/trials", response_model=ClinicalTrialRead, status_code=201)
def create_trial(
    payload: ClinicalTrialCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return ClinicalService(db).create_trial(payload)


@router.get("/trials/{trial_id}", response_model=ClinicalTrialRead)
def get_trial(trial_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ClinicalService(db).get_trial(trial_id)


@router.patch("/trials/{trial_id}", response_model=ClinicalTrialRead)
def update_trial(
    trial_id: str,
    payload: ClinicalTrialUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return ClinicalService(db).update_trial(trial_id, payload)


@router.get("/events", response_model=Page[ClinicalEventRead])
def list_events(
    trial_id: str | None = None,
    event_type: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = ClinicalService(db).list_events(
        pagination.page, pagination.page_size, trial_id=trial_id, event_type=event_type
    )
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/events", response_model=ClinicalEventRead, status_code=201)
def create_event(
    payload: ClinicalEventCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return ClinicalService(db).create_event(payload)
