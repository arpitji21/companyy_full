from decimal import Decimal

from app.schemas.ceo import CEODashboard
from app.services.approval_service import ApprovalService
from app.services.compliance_service import ComplianceService
from app.services.employee_service import EmployeeService
from app.services.finance_service import FinanceService
from app.services.manufacturing_service import ManufacturingService
from app.services.meeting_service import MeetingService
from app.services.notification_service import NotificationService
from app.services.quality_service import QualityService
from app.repositories.project_repository import TaskRepository


class CEODashboardService:
    """
    Pure aggregator: no new tables, just composes what Phase 1/2 already
    built. The two composite scores (company_health_score, risk_score) are a
    documented default formula, not a spec requirement — adjust the weights
    below (or the formula entirely) once you decide how you want them
    calculated; the breakdown fields exist so you can see exactly which
    inputs drove the number instead of trusting a black box.
    """

    def __init__(self, db):
        self.db = db
        self.finance = FinanceService(db)
        self.employees = EmployeeService(db)
        self.compliance = ComplianceService(db)
        self.manufacturing = ManufacturingService(db)
        self.quality = QualityService(db)
        self.approvals = ApprovalService(db)
        self.meetings = MeetingService(db)
        self.notifications = NotificationService(db)
        self.tasks = TaskRepository(db)

    def get_dashboard(self, current_user_id: str) -> CEODashboard:
        finance_summary = self.finance.summary()
        headcount = self.employees.headcount_summary()
        manufacturing_summary = self.manufacturing.summary()
        compliance_summary = self.compliance.summary()
        quality_metrics = self.quality.metrics()
        pending_approvals = self.approvals.pending_count()
        action_items, _ = self.approvals.list(page=1, page_size=10, status="pending")
        upcoming_meetings = self.meetings.upcoming(limit=5)
        unread_notifications = self.notifications.unread_count(current_user_id)
        open_tasks = self.tasks.count_open()

        health_breakdown, health_score = self._company_health_score(
            finance_summary, compliance_summary, manufacturing_summary, pending_approvals
        )
        risk_breakdown, risk_score = self._risk_score(
            finance_summary, compliance_summary, quality_metrics
        )

        return CEODashboard(
            revenue=finance_summary.total_revenue,
            expenses=finance_summary.total_expenses,
            cash_flow=finance_summary.net_cash_flow,
            burn_rate=finance_summary.burn_rate,
            employee_count=headcount["total_employees"],
            hiring_status={
                "active": headcount["active"],
                "onboarding": headcount["onboarding"],
                "on_leave": headcount["on_leave"],
                "terminated": headcount["terminated"],
            },
            open_tasks=open_tasks,
            manufacturing_status=manufacturing_summary.model_dump(),
            compliance_score=compliance_summary.compliance_score,
            pending_approvals=pending_approvals,
            action_items=action_items,
            upcoming_meetings=upcoming_meetings,
            unread_notifications=unread_notifications,
            company_health_score=health_score,
            risk_score=risk_score,
            health_score_breakdown=health_breakdown,
            risk_score_breakdown=risk_breakdown,
            ai_alerts=[],  # Phase 4: populated once AI agents can generate real alerts
        )

    # ------------------------------------------------------------------
    # Default scoring formulas — see class docstring. Weights sum to 1.0.
    # ------------------------------------------------------------------
    @staticmethod
    def _company_health_score(finance_summary, compliance_summary, manufacturing_summary, pending_approvals: int):
        # 1. Compliance: use the score directly (0-100).
        compliance_component = compliance_summary.compliance_score

        # 2. Cash flow: 100 if revenue covers expenses, scaled down toward 0
        #    the further net cash flow is negative relative to revenue.
        revenue = finance_summary.total_revenue
        net = finance_summary.net_cash_flow
        if net >= 0:
            cash_flow_component = 100.0
        elif revenue > 0:
            cash_flow_component = max(0.0, 100.0 + float(net / revenue) * 100.0)
        else:
            cash_flow_component = 0.0

        # 3. Manufacturing: average yield rate, already 0-100.
        manufacturing_component = manufacturing_summary.average_yield_rate or 100.0

        # 4. Operational load: fewer pending approvals piling up == healthier.
        #    Every 5 pending approvals knocks 10 points off, floor at 0.
        approvals_component = max(0.0, 100.0 - (pending_approvals / 5) * 10)

        weights = {
            "compliance": 0.30,
            "cash_flow": 0.30,
            "manufacturing": 0.20,
            "operational_load": 0.20,
        }
        breakdown = {
            "compliance": round(compliance_component, 2),
            "cash_flow": round(cash_flow_component, 2),
            "manufacturing": round(manufacturing_component, 2),
            "operational_load": round(approvals_component, 2),
        }
        score = sum(breakdown[k] * weights[k] for k in weights)
        return breakdown, round(score, 2)

    @staticmethod
    def _risk_score(finance_summary, compliance_summary, quality_metrics):
        # Higher = riskier. Inverse of the health-style components.
        compliance_risk = 100.0 - compliance_summary.compliance_score

        revenue = finance_summary.total_revenue
        net = finance_summary.net_cash_flow
        if net >= 0:
            cash_flow_risk = 0.0
        elif revenue > 0:
            cash_flow_risk = min(100.0, abs(float(net / revenue)) * 100.0)
        else:
            cash_flow_risk = 100.0 if finance_summary.total_expenses > 0 else 0.0

        quality_risk = 100.0 - quality_metrics.pass_rate if quality_metrics.total_checks else 0.0

        weights = {"compliance": 0.4, "cash_flow": 0.3, "quality": 0.3}
        breakdown = {
            "compliance": round(compliance_risk, 2),
            "cash_flow": round(cash_flow_risk, 2),
            "quality": round(quality_risk, 2),
        }
        score = sum(breakdown[k] * weights[k] for k in weights)
        return breakdown, round(score, 2)
