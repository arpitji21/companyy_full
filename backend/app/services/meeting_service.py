from __future__ import annotations

from app.models.meeting import Meeting
from app.repositories.meeting_repository import MeetingRepository
from app.schemas.meeting import MeetingCreate


class MeetingService:
    def __init__(self, db):
        self.db = db
        self.repo = MeetingRepository(db)

    def list(self, page: int, page_size: int, department_id: str | None = None):
        return self.repo.list(page=page, page_size=page_size, department_id=department_id)

    def create(self, data: MeetingCreate) -> Meeting:
        return self.repo.create(Meeting(**data.model_dump()))

    def upcoming(self, limit: int = 10) -> list[Meeting]:
        return self.repo.upcoming(limit)
