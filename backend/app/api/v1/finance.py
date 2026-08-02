from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.finance import (
    BudgetCreate,
    BudgetRead,
    FinanceSummary,
    TransactionCreate,
    TransactionRead,
)
from app.services.finance_service import FinanceService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/finance", tags=["Finance"])


@router.get("/summary", response_model=FinanceSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return FinanceService(db).summary()


@router.get("/transactions", response_model=Page[TransactionRead])
def list_transactions(
    type: str | None = None,
    department_id: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = FinanceService(db).list_transactions(pagination.page, pagination.page_size, type, department_id)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/transactions", response_model=TransactionRead, status_code=201)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Finance")),
):
    return FinanceService(db).create_transaction(payload)


@router.get("/budgets", response_model=Page[BudgetRead])
def list_budgets(
    department_id: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = FinanceService(db).list_budgets(pagination.page, pagination.page_size, department_id)
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/budgets", response_model=BudgetRead, status_code=201)
def create_budget(
    payload: BudgetCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Finance")),
):
    return FinanceService(db).create_budget(payload)
