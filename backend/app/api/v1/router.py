from fastapi import APIRouter

from app.api.v1 import (
    agents,
    analytics,
    approvals,
    auth,
    ceo,
    chat,
    clinical,
    compliance,
    customer,
    departments,
    documents,
    employees,
    finance,
    grant,
    health,
    hr,
    investor,
    manufacturing,
    marketing,
    meetings,
    notifications,
    patent,
    procurement,
    projects,
    quality,
    regulatory,
    research,
    roles,
    sales,
    supplychain,
    tender,
    users,
    workflows,
    ws,
)
from app.api.v1._placeholder import make_placeholder_router

api_router = APIRouter()

# --- Phase 1: fully implemented ---
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(roles.router)
api_router.include_router(departments.router)

# --- Phase 2: fully implemented ---
api_router.include_router(employees.router)
api_router.include_router(documents.router)
api_router.include_router(projects.router)
api_router.include_router(finance.router)
api_router.include_router(hr.router)
api_router.include_router(sales.router)
api_router.include_router(marketing.router)
api_router.include_router(manufacturing.router)
api_router.include_router(quality.router)
api_router.include_router(compliance.router)
api_router.include_router(regulatory.router)
api_router.include_router(supplychain.router)
api_router.include_router(research.router)
api_router.include_router(patent.router)
api_router.include_router(grant.router)

# --- Phase 3: fully implemented ---
api_router.include_router(ceo.router)
api_router.include_router(approvals.router)
api_router.include_router(meetings.router)
api_router.include_router(notifications.router)
api_router.include_router(ws.router)

# --- Phase 4: fully implemented ---
api_router.include_router(agents.router)
api_router.include_router(chat.router)

# --- Phase 5: fully implemented ---
api_router.include_router(customer.router)
api_router.include_router(procurement.router)
api_router.include_router(clinical.router)
api_router.include_router(investor.router)
api_router.include_router(tender.router)
api_router.include_router(analytics.router)

# --- Phase 6: minimal workflow engine (manual trigger, linear steps) ---
api_router.include_router(workflows.router)

# --- Still placeholders ---
_other_modules = [
    ("/settings", "Settings", "Phase 2."),
]

for prefix, tag, note in _other_modules:
    api_router.include_router(make_placeholder_router(prefix, tag, note))

