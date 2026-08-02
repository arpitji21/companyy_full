from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.customer import CustomerSummary, SupportTicketCreate, SupportTicketRead, SupportTicketUpdate
from app.services.customer_service import CustomerService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/customer", tags=["Customer"])


@router.get("/summary", response_model=CustomerSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return CustomerService(db).summary()


@router.get("/tickets", response_model=Page[SupportTicketRead])
def list_tickets(
    status: str | None = None,
    priority: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = CustomerService(db).list(pagination.page, pagination.page_size, status=status, priority=priority)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/tickets", response_model=SupportTicketRead, status_code=201)
def create_ticket(
    payload: SupportTicketCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return CustomerService(db).create(payload)


@router.get("/tickets/{ticket_id}", response_model=SupportTicketRead)
def get_ticket(ticket_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return CustomerService(db).get(ticket_id)


@router.patch("/tickets/{ticket_id}", response_model=SupportTicketRead)
def update_ticket(
    ticket_id: str,
    payload: SupportTicketUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return CustomerService(db).update(ticket_id, payload)
