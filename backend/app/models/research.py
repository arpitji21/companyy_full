from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class ResearchProject(UUIDPKMixin, TimestampMixin, Base):
    """
    The anchor table for the Research module. Patent and Grant both hang a
    `research_project_id` FK off of this once they're built, the same way
    Publication does here — keeps R&D output traceable back to the
    initiative that produced it instead of floating free.
    """

    __tablename__ = "research_projects"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    field: Mapped[str | None] = mapped_column(String(100), nullable=True)  # oncology, cardiology, ...
    status: Mapped[str] = mapped_column(String(30), default="planning")  # planning, active, on_hold, completed
    lead_employee_id: Mapped[str | None] = mapped_column(ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    department_id: Mapped[str | None] = mapped_column(ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)

    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    budget: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    spend: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)

    publications: Mapped[list["Publication"]] = relationship(
        back_populates="research_project", cascade="all, delete-orphan"
    )


class Publication(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "publications"

    research_project_id: Mapped[str | None] = mapped_column(
        ForeignKey("research_projects.id", ondelete="SET NULL"), nullable=True
    )

    title: Mapped[str] = mapped_column(String(500))
    authors: Mapped[str | None] = mapped_column(String(500), nullable=True)
    journal: Mapped[str | None] = mapped_column(String(255), nullable=True)
    publication_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    doi: Mapped[str | None] = mapped_column(String(120), nullable=True)
    citation_count: Mapped[int] = mapped_column(Integer, default=0)

    research_project: Mapped["ResearchProject | None"] = relationship(back_populates="publications")
