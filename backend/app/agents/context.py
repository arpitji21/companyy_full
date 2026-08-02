"""Builds a short, live data snapshot for a department so an agent's
answers are grounded in the real database instead of the model's
imagination. Deliberately reuses the same *_service.summary()/metrics()
methods that already power each department's dashboard — no new queries,
no new tables, just feeding what already exists into the prompt.

Every branch is wrapped so a single broken summary query never breaks
chat: on error we just return "" and the agent answers without the
snapshot rather than the whole request 500ing.
"""

from __future__ import annotations


def build_context(department_slug: str | None, db) -> str:
    slug = (department_slug or "").strip().lower()
    builder = _BUILDERS.get(slug)
    if not builder:
        return ""
    try:
        return builder(db)
    except Exception:
        return ""


def _finance_context(db) -> str:
    from app.services.finance_service import FinanceService

    s = FinanceService(db).summary()
    return (
        "Live finance snapshot — "
        f"total revenue: {s.total_revenue}, total expenses: {s.total_expenses}, "
        f"net cash flow: {s.net_cash_flow}, burn rate: {s.burn_rate}, "
        f"expenses by category: {dict(s.by_category)}."
    )


def _hr_context(db) -> str:
    from app.services.employee_service import EmployeeService

    h = EmployeeService(db).headcount_summary()
    return f"Live HR snapshot — headcount breakdown: {h}."


def _sales_context(db) -> str:
    from app.services.sales_service import SalesService

    s = SalesService(db).summary()
    return (
        "Live sales snapshot — "
        f"total pipeline value: {s.total_pipeline_value}, weighted forecast: {s.weighted_forecast}, "
        f"open deals: {s.open_deals}, won deals: {s.won_deals}, lost deals: {s.lost_deals}, "
        f"by stage: {s.by_stage}."
    )


def _marketing_context(db) -> str:
    from app.services.marketing_service import MarketingService

    s = MarketingService(db).summary()
    return (
        "Live marketing snapshot — "
        f"total campaigns: {s.total_campaigns}, active: {s.active_campaigns}, "
        f"impressions: {s.total_impressions}, clicks: {s.total_clicks}, "
        f"conversions: {s.total_conversions}, avg conversion rate: {s.average_conversion_rate}%."
    )


def _manufacturing_context(db) -> str:
    from app.services.manufacturing_service import ManufacturingService

    s = ManufacturingService(db).summary()
    return f"Live manufacturing snapshot — {s.model_dump()}."


def _quality_context(db) -> str:
    from app.services.quality_service import QualityService

    m = QualityService(db).metrics()
    return (
        "Live quality snapshot — "
        f"total checks: {m.total_checks}, passed: {m.pass_count}, failed: {m.fail_count}, "
        f"pending: {m.pending_count}, pass rate: {m.pass_rate}%."
    )


def _compliance_context(db) -> str:
    from app.services.compliance_service import ComplianceService

    s = ComplianceService(db).summary()
    return (
        "Live compliance snapshot — "
        f"total records: {s.total_records}, approved: {s.approved}, "
        f"expired: {s.expired}, in progress: {s.in_progress}, "
        f"compliance score: {s.compliance_score}%."
    )


def _supplychain_context(db) -> str:
    from app.services.supplychain_service import SupplyChainService

    s = SupplyChainService(db).summary()
    return (
        "Live supply chain snapshot — "
        f"vendors: {s.total_vendors}, SKUs: {s.total_sku_count}, "
        f"items below reorder level: {s.items_below_reorder_level}."
    )


def _projects_context(db) -> str:
    from app.repositories.project_repository import TaskRepository

    open_tasks = TaskRepository(db).count_open()
    return f"Live projects snapshot — open tasks across all projects: {open_tasks}."


def _ceo_context(db) -> str:
    """The CEO agent gets a blend of everything, so 'how are we doing'
    doesn't need the person to pick a department first."""
    parts = []
    for fn in (_finance_context, _hr_context, _manufacturing_context, _compliance_context):
        try:
            text = fn(db)
        except Exception:
            continue
        if text:
            parts.append(text)
    return "\n".join(parts)


_BUILDERS = {
    "finance": _finance_context,
    "hr": _hr_context,
    "sales": _sales_context,
    "marketing": _marketing_context,
    "manufacturing": _manufacturing_context,
    "quality": _quality_context,
    "compliance": _compliance_context,
    "supplychain": _supplychain_context,
    "projects": _projects_context,
    "ceo": _ceo_context,
}
