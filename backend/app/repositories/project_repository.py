from sqlalchemy import func, select

from app.models.project import Project, Task
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    model = Project


class TaskRepository(BaseRepository[Task]):
    model = Task

    def count_open(self) -> int:
        return self.db.scalar(
            select(func.count()).where(Task.status.notin_(["done"]))
        ) or 0
