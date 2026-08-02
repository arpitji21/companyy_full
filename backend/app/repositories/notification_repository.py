from sqlalchemy import func, select, update

from app.models.notification import Notification
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    model = Notification

    def unread_count_for_user(self, user_id: str) -> int:
        return self.db.scalar(
            select(func.count()).where(Notification.user_id == user_id, Notification.is_read.is_(False))
        ) or 0

    def mark_read_by_reference(self, reference_type: str, reference_id: str) -> list[str]:
        """Resolve every notification pointing at a given source record —
        used when that record is actioned directly (e.g. an approval decided
        from the CEO action center), so the notification inbox doesn't keep
        showing a stale 'needs action' item for everyone it went to.

        Returns the distinct user_ids that were affected, so the caller can
        push a live update to each of them."""
        affected = list(
            self.db.scalars(
                select(Notification.user_id).where(
                    Notification.reference_type == reference_type,
                    Notification.reference_id == reference_id,
                    Notification.is_read.is_(False),
                )
            )
        )
        self.db.execute(
            update(Notification)
            .where(
                Notification.reference_type == reference_type,
                Notification.reference_id == reference_id,
                Notification.is_read.is_(False),
            )
            .values(is_read=True)
        )
        self.db.commit()
        return affected
