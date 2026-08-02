from datetime import datetime, timezone

from sqlalchemy import select

from app.models.meeting import Meeting
from app.repositories.base import BaseRepository


class MeetingRepository(BaseRepository[Meeting]):
    model = Meeting

    def upcoming(self, limit: int = 10) -> list[Meeting]:
        now = datetime.now(timezone.utc)
        stmt = (
            select(Meeting)
            .where(Meeting.starts_at >= now, Meeting.status == "scheduled")
            .order_by(Meeting.starts_at.asc())
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())
