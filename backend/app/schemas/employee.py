from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class EmployeeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str | None
    department_id: str | None
    full_name: str
    job_title: str | None
    email: EmailStr
    phone: str | None
    status: str
    employment_type: str
    hire_date: date | None
    manager_id: str | None


class EmployeeCreate(BaseModel):
    full_name: str
    email: EmailStr
    job_title: str | None = None
    department_id: str | None = None
    phone: str | None = None
    employment_type: str = "full_time"
    hire_date: date | None = None
    manager_id: str | None = None
    salary: float | None = None


class EmployeeUpdate(BaseModel):
    full_name: str | None = None
    job_title: str | None = None
    department_id: str | None = None
    phone: str | None = None
    status: str | None = None
    employment_type: str | None = None
    manager_id: str | None = None
    salary: float | None = None


class OrgChartNode(BaseModel):
    id: str
    full_name: str
    job_title: str | None
    department_id: str | None
    reports: list["OrgChartNode"] = []
