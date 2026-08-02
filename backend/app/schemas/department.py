from pydantic import BaseModel, ConfigDict


class DepartmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    slug: str
    icon: str | None
    description: str | None
    head_employee_id: str | None


class DepartmentCreate(BaseModel):
    name: str
    slug: str
    icon: str | None = None
    description: str | None = None


class DepartmentUpdate(BaseModel):
    name: str | None = None
    icon: str | None = None
    description: str | None = None
    head_employee_id: str | None = None
