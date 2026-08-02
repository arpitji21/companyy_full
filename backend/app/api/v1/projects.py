from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.project import (
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
    TaskCreate,
    TaskRead,
    TaskUpdate,
)
from app.services.project_service import ProjectService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=Page[ProjectRead])
def list_projects(
    department_id: str | None = None,
    status: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = ProjectService(db).list(pagination.page, pagination.page_size, department_id, status)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ProjectService(db).get(project_id)


@router.post("", response_model=ProjectRead, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ProjectService(db).create(payload)


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(project_id: str, payload: ProjectUpdate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ProjectService(db).update(project_id, payload)


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    ProjectService(db).delete(project_id)


@router.post("/{project_id}/tasks", response_model=TaskRead, status_code=201)
def create_task(project_id: str, payload: TaskCreate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ProjectService(db).create_task(project_id, payload)


@router.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: str, payload: TaskUpdate, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ProjectService(db).update_task(task_id, payload)


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    ProjectService(db).delete_task(task_id)
