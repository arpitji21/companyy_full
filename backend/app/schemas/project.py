from datetime import date

from pydantic import BaseModel, ConfigDict


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str | None
    assignee_id: str | None
    title: str
    description: str | None
    status: str
    priority: str
    due_date: date | None


class TaskCreate(BaseModel):
    project_id: str | None = None
    assignee_id: str | None = None
    title: str
    description: str | None = None
    status: str = "todo"
    priority: str = "medium"
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    assignee_id: str | None = None
    due_date: date | None = None


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None
    department_id: str | None
    owner_id: str | None
    status: str
    start_date: date | None
    due_date: date | None
    tasks: list[TaskRead] = []


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    department_id: str | None = None
    owner_id: str | None = None
    status: str = "planning"
    start_date: date | None = None
    due_date: date | None = None


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None
    owner_id: str | None = None
    due_date: date | None = None
