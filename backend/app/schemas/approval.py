from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ApprovalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    requested_by: str | None
    department_id: str | None
    amount: Decimal | None
    status: str
    approver_id: str | None
    notes: str | None


class ApprovalCreate(BaseModel):
    title: str
    department_id: str | None = None
    amount: Decimal | None = None
    notes: str | None = None


class ApprovalDecision(BaseModel):
    approve: bool
    notes: str | None = None
