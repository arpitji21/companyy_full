from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.sales import CustomerCreate, CustomerRead, DealCreate, DealRead, DealUpdate, SalesSummary
from app.services.sales_service import SalesService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.get("/summary", response_model=SalesSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return SalesService(db).summary()


@router.get("/customers", response_model=Page[CustomerRead])
def list_customers(pagination: PaginationParams = Depends(), db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    items, total = SalesService(db).list_customers(pagination.page, pagination.page_size)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/customers", response_model=CustomerRead, status_code=201)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Sales")),
):
    return SalesService(db).create_customer(payload)


@router.get("/deals", response_model=Page[DealRead])
def list_deals(
    stage: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = SalesService(db).list_deals(pagination.page, pagination.page_size, stage)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/deals", response_model=DealRead, status_code=201)
def create_deal(payload: DealCreate, db: Session = Depends(get_db), _=Depends(require_roles("CEO", "Admin", "Sales"))):
    return SalesService(db).create_deal(payload)


@router.patch("/deals/{deal_id}", response_model=DealRead)
def update_deal(
    deal_id: str,
    payload: DealUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Sales")),
):
    return SalesService(db).update_deal(deal_id, payload)
