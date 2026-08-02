from app.core.exceptions import AppError, NotFoundError
from app.models.workflow import Workflow, WorkflowRun
from app.repositories.workflow_repository import (
    WorkflowRepository,
    WorkflowRunRepository,
    WorkflowStepRunRepository,
)
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate
from app.tasks import safe_delay


class WorkflowService:
    def __init__(self, db):
        self.db = db
        self.workflows = WorkflowRepository(db)
        self.runs = WorkflowRunRepository(db)
        self.step_runs = WorkflowStepRunRepository(db)

    def list(self, page: int, page_size: int, is_active: bool | None = None):
        return self.workflows.list(page=page, page_size=page_size, is_active=is_active)

    def get(self, workflow_id: str) -> Workflow:
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            raise NotFoundError("Workflow not found.")
        return workflow

    def create(self, data: WorkflowCreate) -> Workflow:
        workflow = Workflow(
            name=data.name,
            description=data.description,
            trigger_type=data.trigger_type,
            schedule_cron=data.schedule_cron,
            is_active=data.is_active,
            steps=[step.model_dump() for step in data.steps],
        )
        return self.workflows.create(workflow)

    def update(self, workflow_id: str, data: WorkflowUpdate) -> Workflow:
        workflow = self.get(workflow_id)
        update_data = data.model_dump(exclude_unset=True)
        if "steps" in update_data and update_data["steps"] is not None:
            update_data["steps"] = [
                step if isinstance(step, dict) else step.model_dump() for step in update_data["steps"]
            ]
        return self.workflows.update(workflow, update_data)

    def trigger_run(self, workflow_id: str, *, triggered_by: str) -> WorkflowRun:
        workflow = self.get(workflow_id)
        if not workflow.is_active:
            raise AppError(
                "This workflow is inactive and can't be run.", status_code=400, error_code="workflow_inactive"
            )
        if not workflow.steps:
            raise AppError("This workflow has no steps to run.", status_code=400, error_code="workflow_empty")

        run = self.runs.create(WorkflowRun(workflow_id=workflow.id, status="pending", triggered_by=triggered_by))

        # Imported lazily to avoid a hard import-time dependency between the
        # request path and the Celery task module (mirrors app/tasks/reports.py).
        from app.tasks.workflows import execute_workflow_run

        safe_delay(execute_workflow_run, run.id)
        return run

    def list_runs(self, workflow_id: str, page: int, page_size: int):
        self.get(workflow_id)  # 404s if the workflow doesn't exist
        return self.runs.list_for_workflow(workflow_id, page=page, page_size=page_size)

    def get_run_detail(self, run_id: str):
        run = self.runs.get(run_id)
        if not run:
            raise NotFoundError("Workflow run not found.")
        step_runs = self.step_runs.list_for_run(run_id)
        return run, step_runs
