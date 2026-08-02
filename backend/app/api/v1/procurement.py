from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.procurement import (
    ProcurementSummary,
    PurchaseOrderCreate,
    PurchaseOrderRead,
    PurchaseOrderUpdate,
)
from app.services.procurement_service import ProcurementService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/procurement", tags=["Procurement"])


@router.get("/summary", response_model=ProcurementSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ProcurementService(db).summary()


@router.get("/orders", response_model=Page[PurchaseOrderRead])
def list_orders(
    status: str | None = None,
    category: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = ProcurementService(db).list(
        pagination.page, pagination.page_size, status=status, category=category
    )
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/orders", response_model=PurchaseOrderRead, status_code=201)
def create_order(
    payload: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return ProcurementService(db).create(payload)


@router.get("/orders/{order_id}", response_model=PurchaseOrderRead)
def get_order(order_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ProcurementService(db).get(order_id)


@router.patch("/orders/{order_id}", response_model=PurchaseOrderRead)
def update_order(
    order_id: str,
    payload: PurchaseOrderUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return ProcurementService(db).update(order_id, payload)
