from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SupportTicketRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    customer_id: str | None
    account_owner_id: str | None
    subject: str
    description: str | None
    status: str
    priority: str
    sla_due_at: datetime | None
    resolved_at: datetime | None
    escalated_at: datetime | None
    csat_score: Decimal | None


class SupportTicketCreate(BaseModel):
    customer_id: str | None = None
    account_owner_id: str | None = None
    subject: str
    description: str | None = None
    status: str = "open"
    priority: str = "medium"
    sla_due_at: datetime | None = None


class SupportTicketUpdate(BaseModel):
    status: str | None = None
    priority: str | None = None
    account_owner_id: str | None = None
    resolved_at: datetime | None = None
    escalated_at: datetime | None = None
    csat_score: Decimal | None = None


class CustomerSummary(BaseModel):
    total_tickets: int
    open_tickets: int
    escalated_tickets: int
    resolved_tickets: int
    breached_sla: int  # open tickets whose sla_due_at has already passed
    average_csat: float | None
    at_risk_customers: int  # customers.churn_risk == "high"
