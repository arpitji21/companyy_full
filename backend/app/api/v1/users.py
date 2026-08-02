from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user_service import UserService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=Page[UserRead])
def list_users(
    department_id: str | None = None,
    role_id: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin")),
):
    items, total = UserService(db).list(pagination.page, pagination.page_size, department_id, role_id)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return UserService(db).get(user_id)


@router.post("", response_model=UserRead, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db), _=Depends(require_roles("CEO", "Admin"))):
    return UserService(db).create(payload)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin")),
):
    return UserService(db).update(user_id, payload)


@router.delete("/{user_id}", response_model=UserRead)
def deactivate_user(user_id: str, db: Session = Depends(get_db), _=Depends(require_roles("CEO", "Admin"))):
    return UserService(db).deactivate(user_id)
