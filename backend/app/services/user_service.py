from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def get(self, user_id: str) -> User:
        user = self.repo.get(user_id)
        if not user:
            raise NotFoundError("User not found.")
        return user

    def list(self, page: int, page_size: int, department_id: str | None = None, role_id: str | None = None):
        return self.repo.list(page=page, page_size=page_size, department_id=department_id, role_id=role_id)

    def create(self, data: UserCreate) -> User:
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role_id=data.role_id,
            department_id=data.department_id,
        )
        return self.repo.create(user)

    def update(self, user_id: str, data: UserUpdate) -> User:
        user = self.get(user_id)
        return self.repo.update(user, data.model_dump(exclude_unset=True))

    def deactivate(self, user_id: str) -> User:
        user = self.get(user_id)
        return self.repo.update(user, {"is_active": False})
