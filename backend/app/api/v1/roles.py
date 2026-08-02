from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.db.session import get_db
from app.models.user import Role
from app.repositories.role_repository import RoleRepository
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("", response_model=list[RoleRead])
def list_roles(db: Session = Depends(get_db), _=Depends(require_roles("CEO", "Admin"))):
    items, _total = RoleRepository(db).list(page=1, page_size=100)
    return items


@router.post("", response_model=RoleRead, status_code=201)
def create_role(payload: RoleCreate, db: Session = Depends(get_db), _=Depends(require_roles("CEO", "Admin"))):
    repo = RoleRepository(db)
    if repo.get_by_name(payload.name):
        raise AlreadyExistsError(f"Role '{payload.name}' already exists.")

    role = Role(name=payload.name, description=payload.description)
    role.permissions = repo.get_permissions_by_codes(payload.permission_codes)
    return repo.create(role)


@router.patch("/{role_id}", response_model=RoleRead)
def update_role(role_id: str, payload: RoleUpdate, db: Session = Depends(get_db), _=Depends(require_roles("CEO", "Admin"))):
    repo = RoleRepository(db)
    role = repo.get(role_id)
    if not role:
        raise NotFoundError("Role not found.")

    if payload.description is not None:
        role.description = payload.description
    if payload.permission_codes is not None:
        role.permissions = repo.get_permissions_by_codes(payload.permission_codes)

    db.commit()
    db.refresh(role)
    return role
