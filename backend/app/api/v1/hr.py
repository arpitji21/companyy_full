from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.db.session import get_db
from app.schemas.employee import OrgChartNode
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/hr", tags=["HR"])


@router.get("/headcount", summary="Headcount summary by status and department")
def headcount(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return EmployeeService(db).headcount_summary()


@router.get("/org-chart", response_model=list[OrgChartNode])
def org_chart(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return EmployeeService(db).org_chart()


# NOTE: Attendance, Leave, Recruitment/Hiring Pipeline, Performance Reviews,
# Payroll Summary, and Training aren't in the Phase 1 schema yet — they need
# their own tables (attendance_records, leave_requests, job_openings,
# performance_reviews, payroll_runs, trainings) before they can be built for
# real. Tracked as a Phase 2 follow-up migration rather than stubbed here
# with fake data.
