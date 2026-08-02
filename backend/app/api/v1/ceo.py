from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.db.session import get_db
from app.schemas.ceo import CEODashboard
from app.services.ceo_service import CEODashboardService

router = APIRouter(prefix="/ceo", tags=["CEO Dashboard"])


@router.get("/dashboard", response_model=CEODashboard)
def get_dashboard(db: Session = Depends(get_db), user=Depends(require_roles("CEO", "Admin"))):
    return CEODashboardService(db).get_dashboard(current_user_id=user.id)
