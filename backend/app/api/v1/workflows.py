from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowRead,
    WorkflowRunDetail,
    WorkflowRunRead,
    WorkflowStepRunRead,
    WorkflowUpdate,
)
from app.services.workflow_service import WorkflowService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/workflows", tags=["Workflows"])

# Open to any authenticated user for now, matching most other department
# modules (Sales, Marketing, Manufacturing, ...) rather than the stricter
# CEO/Admin-only gate on Departments or Employees. Tighten with
# require_roles(...) later if workflow definitions need to be locked down.


@router.get("", response_model=Page[WorkflowRead])
def list_workflows(
    is_active: bool | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = WorkflowService(db).list(pagination.page, pagination.page_size, is_active)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("", response_model=WorkflowRead, status_code=201)
def create_workflow(
    payload: WorkflowCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return WorkflowService(db).create(payload)


@router.get("/{workflow_id}", response_model=WorkflowRead)
def get_workflow(workflow_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return WorkflowService(db).get(workflow_id)


@router.patch("/{workflow_id}", response_model=WorkflowRead)
def update_workflow(
    workflow_id: str,
    payload: WorkflowUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return WorkflowService(db).update(workflow_id, payload)


@router.post("/{workflow_id}/run", response_model=WorkflowRunRead, status_code=202)
def run_workflow(
    workflow_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user),
):
    """Triggers a manual run. Returns immediately with status="pending" —
    the steps execute in the background via Celery (app/tasks/workflows.py);
    poll GET /workflows/runs/{run_id} for progress."""
    return WorkflowService(db).trigger_run(workflow_id, triggered_by=user.id)


@router.get("/{workflow_id}/runs", response_model=Page[WorkflowRunRead])
def list_workflow_runs(
    workflow_id: str,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = WorkflowService(db).list_runs(workflow_id, pagination.page, pagination.page_size)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.get("/runs/{run_id}", response_model=WorkflowRunDetail)
def get_workflow_run(run_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    run, step_runs = WorkflowService(db).get_run_detail(run_id)
    return WorkflowRunDetail(
        **WorkflowRunRead.model_validate(run).model_dump(),
        step_runs=[WorkflowStepRunRead.model_validate(s) for s in step_runs],
    )
