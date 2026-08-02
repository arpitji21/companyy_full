from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PublicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    research_project_id: str | None
    title: str
    authors: str | None
    journal: str | None
    publication_date: date | None
    doi: str | None
    citation_count: int


class PublicationCreate(BaseModel):
    research_project_id: str | None = None
    title: str
    authors: str | None = None
    journal: str | None = None
    publication_date: date | None = None
    doi: str | None = None
    citation_count: int = 0


class ResearchProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str | None
    field: str | None
    status: str
    lead_employee_id: str | None
    department_id: str | None
    start_date: date | None
    end_date: date | None
    budget: Decimal | None
    spend: Decimal
    publications: list[PublicationRead] = []


class ResearchProjectCreate(BaseModel):
    title: str
    description: str | None = None
    field: str | None = None
    status: str = "planning"
    lead_employee_id: str | None = None
    department_id: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    budget: Decimal | None = None
    spend: Decimal = Decimal("0")


class ResearchProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    field: str | None = None
    status: str | None = None
    lead_employee_id: str | None = None
    end_date: date | None = None
    budget: Decimal | None = None
    spend: Decimal | None = None


class ResearchSummary(BaseModel):
    total_projects: int
    active_projects: int
    completed_projects: int
    total_publications: int
    total_citations: int
    total_budget: Decimal
    total_spend: Decimal
    budget_utilization: float  # % of total_budget spent
