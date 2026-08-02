from app.core.exceptions import NotFoundError
from app.models.project import Project, Task
from app.repositories.project_repository import ProjectRepository, TaskRepository
from app.schemas.project import ProjectCreate, ProjectUpdate, TaskCreate, TaskUpdate


class ProjectService:
    def __init__(self, db):
        self.db = db
        self.projects = ProjectRepository(db)
        self.tasks = TaskRepository(db)

    def get(self, project_id: str) -> Project:
        project = self.projects.get(project_id)
        if not project:
            raise NotFoundError("Project not found.")
        return project

    def list(self, page: int, page_size: int, department_id: str | None = None, status: str | None = None):
        return self.projects.list(page=page, page_size=page_size, department_id=department_id, status=status)

    def create(self, data: ProjectCreate) -> Project:
        return self.projects.create(Project(**data.model_dump()))

    def update(self, project_id: str, data: ProjectUpdate) -> Project:
        project = self.get(project_id)
        return self.projects.update(project, data.model_dump(exclude_unset=True))

    def delete(self, project_id: str) -> None:
        self.projects.delete(self.get(project_id))

    # --- Tasks (nested under a project) ---
    def get_task(self, task_id: str) -> Task:
        task = self.tasks.get(task_id)
        if not task:
            raise NotFoundError("Task not found.")
        return task

    def create_task(self, project_id: str, data: TaskCreate) -> Task:
        self.get(project_id)  # 404s if the project doesn't exist
        return self.tasks.create(Task(project_id=project_id, **data.model_dump(exclude={"project_id"})))

    def update_task(self, task_id: str, data: TaskUpdate) -> Task:
        task = self.get_task(task_id)
        return self.tasks.update(task, data.model_dump(exclude_unset=True))

    def delete_task(self, task_id: str) -> None:
        self.tasks.delete(self.get_task(task_id))
