from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.supplychain import (
    InventoryItemCreate,
    InventoryItemRead,
    InventoryItemUpdate,
    SupplyChainSummary,
    VendorCreate,
    VendorRead,
)
from app.services.supplychain_service import SupplyChainService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/supply-chain", tags=["Supply Chain"])


@router.get("/summary", response_model=SupplyChainSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return SupplyChainService(db).summary()


@router.get("/vendors", response_model=Page[VendorRead])
def list_vendors(pagination: PaginationParams = Depends(), db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    items, total = SupplyChainService(db).list_vendors(pagination.page, pagination.page_size)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/vendors", response_model=VendorRead, status_code=201)
def create_vendor(
    payload: VendorCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return SupplyChainService(db).create_vendor(payload)


@router.get("/inventory", response_model=Page[InventoryItemRead])
def list_inventory(pagination: PaginationParams = Depends(), db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    items, total = SupplyChainService(db).list_inventory(pagination.page, pagination.page_size)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/inventory", response_model=InventoryItemRead, status_code=201)
def create_inventory_item(
    payload: InventoryItemCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return SupplyChainService(db).create_inventory_item(payload)


@router.patch("/inventory/{item_id}", response_model=InventoryItemRead)
def update_inventory_item(
    item_id: str,
    payload: InventoryItemUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return SupplyChainService(db).update_inventory_item(item_id, payload)
