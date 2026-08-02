from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.department import DepartmentCreate, DepartmentRead, DepartmentUpdate
from app.services.department_service import DepartmentService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("", response_model=Page[DepartmentRead])
def list_departments(
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = DepartmentService(db).list(pagination.page, pagination.page_size)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.get("/{department_id}", response_model=DepartmentRead)
def get_department(department_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return DepartmentService(db).get(department_id)


@router.post("", response_model=DepartmentRead, status_code=201)
def create_department(
    payload: DepartmentCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin")),
):
    return DepartmentService(db).create(payload)


@router.patch("/{department_id}", response_model=DepartmentRead)
def update_department(
    department_id: str,
    payload: DepartmentUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin")),
):
    return DepartmentService(db).update(department_id, payload)


@router.delete("/{department_id}", status_code=204)
def delete_department(
    department_id: str,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin")),
):
    DepartmentService(db).delete(department_id)
