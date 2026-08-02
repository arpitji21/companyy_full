from decimal import Decimal

from app.core.exceptions import NotFoundError
from app.models.research import Publication, ResearchProject
from app.repositories.research_repository import PublicationRepository, ResearchProjectRepository
from app.schemas.research import (
    PublicationCreate,
    ResearchProjectCreate,
    ResearchProjectUpdate,
    ResearchSummary,
)


class ResearchService:
    def __init__(self, db):
        self.db = db
        self.projects = ResearchProjectRepository(db)
        self.publications = PublicationRepository(db)

    # --- projects ---
    def list_projects(self, page: int, page_size: int, status: str | None = None, field: str | None = None):
        return self.projects.list(page=page, page_size=page_size, status=status, field=field)

    def get_project(self, project_id: str) -> ResearchProject:
        project = self.projects.get(project_id)
        if not project:
            raise NotFoundError("Research project not found.")
        return project

    def create_project(self, data: ResearchProjectCreate) -> ResearchProject:
        return self.projects.create(ResearchProject(**data.model_dump()))

    def update_project(self, project_id: str, data: ResearchProjectUpdate) -> ResearchProject:
        project = self.get_project(project_id)
        return self.projects.update(project, data.model_dump(exclude_unset=True))

    # --- publications ---
    def list_publications(self, page: int, page_size: int, research_project_id: str | None = None):
        return self.publications.list(page=page, page_size=page_size, research_project_id=research_project_id)

    def create_publication(self, data: PublicationCreate) -> Publication:
        return self.publications.create(Publication(**data.model_dump()))

    # --- summary ---
    def summary(self) -> ResearchSummary:
        by_status = self.projects.counts_by_status()
        total_projects = sum(by_status.values())
        budget_total, spend_total = self.projects.totals()
        utilization = float(spend_total / budget_total * 100) if budget_total else 0.0

        return ResearchSummary(
            total_projects=total_projects,
            active_projects=by_status.get("active", 0),
            completed_projects=by_status.get("completed", 0),
            total_publications=self.publications.list(page=1, page_size=1)[1],
            total_citations=self.publications.total_citations(),
            total_budget=Decimal(budget_total),
            total_spend=Decimal(spend_total),
            budget_utilization=round(utilization, 2),
        )
