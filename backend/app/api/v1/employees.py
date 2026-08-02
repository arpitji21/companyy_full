from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.employee import EmployeeCreate, EmployeeRead, EmployeeUpdate
from app.services.employee_service import EmployeeService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("", response_model=Page[EmployeeRead])
def list_employees(
    department_id: str | None = None,
    status: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = EmployeeService(db).list(pagination.page, pagination.page_size, department_id, status)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(employee_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return EmployeeService(db).get(employee_id)


@router.post("", response_model=EmployeeRead, status_code=201)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "HR")),
):
    return EmployeeService(db).create(payload)


@router.patch("/{employee_id}", response_model=EmployeeRead)
def update_employee(
    employee_id: str,
    payload: EmployeeUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "HR")),
):
    return EmployeeService(db).update(employee_id, payload)


@router.delete("/{employee_id}", response_model=EmployeeRead)
def terminate_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "HR")),
):
    return EmployeeService(db).terminate(employee_id)
