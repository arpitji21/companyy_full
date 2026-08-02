from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.analytics import AnalyticsSummary, ReportCreate, ReportRead
from app.schemas.common import Page
from app.services.analytics_service import AnalyticsService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# NOTE: `/summary` blends live numbers already computed by Finance, Sales,
# Manufacturing, and Compliance's own services rather than a separate
# warehouse — see AnalyticsService's docstring. Creating a report (POST
# /reports) returns immediately; a Celery task (app/tasks/reports.py)
# builds the actual snapshot and uploads it to object storage in the
# background, filling in `s3_key` once done. Scheduled/recurring report
# generation (e.g. "every Monday") isn't built yet — only on-demand.


@router.get("/summary", response_model=AnalyticsSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return AnalyticsService(db).summary()


@router.get("/reports", response_model=Page[ReportRead])
def list_reports(
    report_type: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = AnalyticsService(db).list_reports(
        pagination.page, pagination.page_size, report_type=report_type
    )
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/reports", response_model=ReportRead, status_code=201)
def create_report(
    payload: ReportCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("CEO", "Admin", "Manager")),
):
    return AnalyticsService(db).create_report(payload, generated_by=user.id)


@router.get("/reports/{report_id}", response_model=ReportRead)
def get_report(report_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return AnalyticsService(db).get_report(report_id)
