from decimal import Decimal

from sqlalchemy import func, select

from app.models.research import Publication, ResearchProject
from app.repositories.base import BaseRepository


class ResearchProjectRepository(BaseRepository[ResearchProject]):
    model = ResearchProject

    def counts_by_status(self) -> dict[str, int]:
        rows = self.db.execute(
            select(ResearchProject.status, func.count()).group_by(ResearchProject.status)
        ).all()
        return {status: count for status, count in rows}

    def totals(self) -> tuple[Decimal, Decimal]:
        budget_total = self.db.scalar(select(func.coalesce(func.sum(ResearchProject.budget), 0))) or Decimal("0")
        spend_total = self.db.scalar(select(func.coalesce(func.sum(ResearchProject.spend), 0))) or Decimal("0")
        return Decimal(budget_total), Decimal(spend_total)


class PublicationRepository(BaseRepository[Publication]):
    model = Publication

    def total_citations(self) -> int:
        return self.db.scalar(select(func.coalesce(func.sum(Publication.citation_count), 0))) or 0
