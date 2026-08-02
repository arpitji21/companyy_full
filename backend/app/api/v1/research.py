from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.research import (
    PublicationCreate,
    PublicationRead,
    ResearchProjectCreate,
    ResearchProjectRead,
    ResearchProjectUpdate,
    ResearchSummary,
)
from app.services.research_service import ResearchService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/research", tags=["Research"])


@router.get("/summary", response_model=ResearchSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ResearchService(db).summary()


@router.get("/projects", response_model=Page[ResearchProjectRead])
def list_projects(
    status: str | None = None,
    field: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = ResearchService(db).list_projects(
        pagination.page, pagination.page_size, status=status, field=field
    )
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/projects", response_model=ResearchProjectRead, status_code=201)
def create_project(
    payload: ResearchProjectCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Research")),
):
    return ResearchService(db).create_project(payload)


@router.get("/projects/{project_id}", response_model=ResearchProjectRead)
def get_project(project_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return ResearchService(db).get_project(project_id)


@router.patch("/projects/{project_id}", response_model=ResearchProjectRead)
def update_project(
    project_id: str,
    payload: ResearchProjectUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Research")),
):
    return ResearchService(db).update_project(project_id, payload)


@router.get("/publications", response_model=Page[PublicationRead])
def list_publications(
    research_project_id: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = ResearchService(db).list_publications(
        pagination.page, pagination.page_size, research_project_id=research_project_id
    )
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/publications", response_model=PublicationRead, status_code=201)
def create_publication(
    payload: PublicationCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin", "Research")),
):
    return ResearchService(db).create_publication(payload)
