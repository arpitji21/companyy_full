from decimal import Decimal

from pydantic import BaseModel

from app.schemas.approval import ApprovalRead
from app.schemas.employee import OrgChartNode  # noqa: F401  (kept available for future org-chart widget reuse)
from app.schemas.meeting import MeetingRead


class CEODashboard(BaseModel):
    # --- Finance ---
    revenue: Decimal
    expenses: Decimal
    cash_flow: Decimal
    burn_rate: Decimal

    # --- People ---
    employee_count: int
    hiring_status: dict[str, int]  # by employee status: active/onboarding/on_leave/terminated

    # --- Operations ---
    open_tasks: int
    manufacturing_status: dict
    compliance_score: float

    # --- Governance / attention items ---
    pending_approvals: int
    # The actual pending requests (HR, Finance, Procurement, ...) so the CEO
    # can approve/reject right here, without opening the owning department's
    # page. Capped — see CEODashboardService.
    action_items: list[ApprovalRead]
    upcoming_meetings: list[MeetingRead]
    unread_notifications: int

    # --- Composite scores ---
    company_health_score: float
    risk_score: float
    health_score_breakdown: dict[str, float]
    risk_score_breakdown: dict[str, float]

    # --- Not yet available ---
    ai_alerts: list[str]  # always empty until Phase 4 (AI agents) exists
