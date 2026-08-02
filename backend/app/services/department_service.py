from sqlalchemy.orm import Session

from app.core.exceptions import AlreadyExistsError, NotFoundError
from app.models.department import Department
from app.repositories.department_repository import DepartmentRepository
from app.schemas.department import DepartmentCreate, DepartmentUpdate


class DepartmentService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = DepartmentRepository(db)

    def get(self, department_id: str) -> Department:
        dept = self.repo.get(department_id)
        if not dept:
            raise NotFoundError("Department not found.")
        return dept

    def list(self, page: int, page_size: int):
        return self.repo.list(page=page, page_size=page_size)

    def create(self, data: DepartmentCreate) -> Department:
        if self.repo.get_by_slug(data.slug):
            raise AlreadyExistsError(f"Department with slug '{data.slug}' already exists.")
        dept = Department(**data.model_dump())
        return self.repo.create(dept)

    def update(self, department_id: str, data: DepartmentUpdate) -> Department:
        dept = self.get(department_id)
        return self.repo.update(dept, data.model_dump(exclude_unset=True))

    def delete(self, department_id: str) -> None:
        dept = self.get(department_id)
        self.repo.delete(dept)
