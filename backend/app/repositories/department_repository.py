from sqlalchemy import select

from app.models.department import Department
from app.repositories.base import BaseRepository


class DepartmentRepository(BaseRepository[Department]):
    model = Department

    def get_by_slug(self, slug: str) -> Department | None:
        return self.db.scalar(select(Department).where(Department.slug == slug))
