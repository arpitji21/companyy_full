from app.core.exceptions import NotFoundError
from app.models.customer_support import SupportTicket
from app.repositories.customer_repository import SupportTicketRepository
from app.schemas.customer import CustomerSummary, SupportTicketCreate, SupportTicketUpdate


class CustomerService:
    def __init__(self, db):
        self.db = db
        self.repo = SupportTicketRepository(db)

    def list(self, page: int, page_size: int, status: str | None = None, priority: str | None = None):
        return self.repo.list(page=page, page_size=page_size, status=status, priority=priority)

    def get(self, ticket_id: str) -> SupportTicket:
        ticket = self.repo.get(ticket_id)
        if not ticket:
            raise NotFoundError("Support ticket not found.")
        return ticket

    def create(self, data: SupportTicketCreate) -> SupportTicket:
        return self.repo.create(SupportTicket(**data.model_dump()))

    def update(self, ticket_id: str, data: SupportTicketUpdate) -> SupportTicket:
        ticket = self.get(ticket_id)
        return self.repo.update(ticket, data.model_dump(exclude_unset=True))

    def summary(self) -> CustomerSummary:
        by_status = self.repo.counts_by_status()
        return CustomerSummary(
            total_tickets=sum(by_status.values()),
            open_tickets=by_status.get("open", 0) + by_status.get("pending", 0),
            escalated_tickets=by_status.get("escalated", 0),
            resolved_tickets=by_status.get("resolved", 0) + by_status.get("closed", 0),
            breached_sla=self.repo.breached_sla_count(),
            average_csat=self.repo.average_csat(),
            at_risk_customers=self.repo.at_risk_customer_count(),
        )
