from app.core.exceptions import NotFoundError
from app.models.workflow import Approval
from app.repositories.approval_repository import ApprovalRepository
from app.repositories.user_repository import UserRepository
from app.schemas.approval import ApprovalCreate, ApprovalDecision
from app.services.notification_service import NotificationService

# Roles that should see "needs your decision" notifications for approvals
# raised anywhere in the company (HR, Finance, Procurement, etc.), so the
# CEO never has to open the originating department's page to act on them.
APPROVAL_NOTIFY_ROLES = ["CEO", "Admin"]


class ApprovalService:
    def __init__(self, db):
        self.db = db
        self.repo = ApprovalRepository(db)
        self.notifications = NotificationService(db)
        self.users = UserRepository(db)

    def list(self, page: int, page_size: int, status: str | None = None):
        return self.repo.list(page=page, page_size=page_size, status=status)

    def create(self, data: ApprovalCreate, requested_by: str) -> Approval:
        approval = Approval(requested_by=requested_by, **data.model_dump())
        approval = self.repo.create(approval)

        self.notifications.notify_role(
            APPROVAL_NOTIFY_ROLES,
            type="approval_needed",
            title=f"Approval needed: {approval.title}",
            body=approval.notes,
            link="/app/approvals",
            reference_type="approval",
            reference_id=approval.id,
        )
        self._dispatch_approval_emails(approval)
        return approval

    def _dispatch_approval_emails(self, approval: Approval) -> None:
        # Approvals are time-sensitive and recipients may not have the app
        # open, so back the in-app notification above with an email too —
        # one background task per recipient (see send_approval_needed_email's
        # docstring for why not one task looping over all of them).
        from app.tasks import safe_delay
        from app.tasks.email import send_approval_needed_email

        recipients = self.users.list_by_role_names(APPROVAL_NOTIFY_ROLES)
        for recipient in recipients:
            safe_delay(send_approval_needed_email, recipient.email, approval.title, approval.notes)

    def decide(self, approval_id: str, data: ApprovalDecision, approver_id: str) -> Approval:
        approval = self.repo.get(approval_id)
        if not approval:
            raise NotFoundError("Approval not found.")
        approval = self.repo.update(
            approval,
            {
                "status": "approved" if data.approve else "rejected",
                "approver_id": approver_id,
                "notes": data.notes,
            },
        )
        # Clears the "needs your decision" notification for everyone it went
        # to, wherever they act on it from (dashboard, inbox, or this page).
        self.notifications.resolve_reference("approval", approval_id)
        return approval

    def pending_count(self) -> int:
        return self.repo.count_pending()
