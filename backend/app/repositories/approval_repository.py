from sqlalchemy import func, select

from app.models.workflow import Approval
from app.repositories.base import BaseRepository


class ApprovalRepository(BaseRepository[Approval]):
    model = Approval

    def count_pending(self) -> int:
        return self.db.scalar(select(func.count()).where(Approval.status == "pending")) or 0
