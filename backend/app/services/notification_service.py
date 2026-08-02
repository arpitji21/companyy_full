from app.core.exceptions import NotFoundError
from app.models.notification import Notification
from app.repositories.notification_repository import NotificationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.notification import NotificationCreate, NotificationRead
from app.websocket.publisher import publish_notification


class NotificationService:
    def __init__(self, db):
        self.db = db
        self.repo = NotificationRepository(db)
        self.users = UserRepository(db)

    def list_for_user(self, user_id: str, page: int, page_size: int, unread_only: bool = False):
        filters = {"user_id": user_id}
        if unread_only:
            filters["is_read"] = False
        return self.repo.list(page=page, page_size=page_size, **filters)

    def create(self, data: NotificationCreate) -> Notification:
        notification = self.repo.create(Notification(**data.model_dump()))
        self._push(notification)
        return notification

    def mark_read(self, notification_id: str, user_id: str) -> Notification:
        notification = self.repo.get(notification_id)
        if not notification or notification.user_id != user_id:
            raise NotFoundError("Notification not found.")
        return self.repo.update(notification, {"is_read": True})

    def unread_count(self, user_id: str) -> int:
        return self.repo.unread_count_for_user(user_id)

    def notify_role(
        self,
        role_names: list[str],
        *,
        type: str,
        title: str,
        body: str | None = None,
        link: str | None = None,
        reference_type: str | None = None,
        reference_id: str | None = None,
    ) -> list[Notification]:
        """Fan a notification out to every active user holding one of
        role_names — e.g. every request that needs CEO sign-off calls this
        with role_names=["CEO", "Admin"] so it shows up in their inbox and
        (via reference_type/reference_id) can be actioned right there."""
        recipients = self.users.list_by_role_names(role_names)
        created = []
        for recipient in recipients:
            notification = Notification(
                user_id=recipient.id,
                type=type,
                title=title,
                body=body,
                link=link,
                reference_type=reference_type,
                reference_id=reference_id,
            )
            notification = self.repo.create(notification)
            self._push(notification)
            created.append(notification)
        return created

    def resolve_reference(self, reference_type: str, reference_id: str) -> None:
        """Mark every notification pointing at a source record as read once
        that record has been actioned (e.g. an approval decided)."""
        affected_user_ids = self.repo.mark_read_by_reference(reference_type, reference_id)
        for user_id in affected_user_ids:
            publish_notification(
                user_id,
                {
                    "kind": "notification.resolved",
                    "reference_type": reference_type,
                    "reference_id": reference_id,
                },
            )

    def _push(self, notification: Notification) -> None:
        """Fire the real-time nudge for a freshly committed notification.
        Called after the DB commit, never instead of it — see
        app/websocket/publisher.py for why this is fire-and-forget."""
        publish_notification(
            notification.user_id,
            {
                "kind": "notification.created",
                "notification": NotificationRead.model_validate(notification).model_dump(mode="json"),
            },
        )
