from sqlalchemy import select

from app.models.workflow import Workflow, WorkflowRun, WorkflowStepRun
from app.repositories.base import BaseRepository


class WorkflowRepository(BaseRepository[Workflow]):
    model = Workflow


class WorkflowRunRepository(BaseRepository[WorkflowRun]):
    model = WorkflowRun

    def list_for_workflow(self, workflow_id: str, *, page: int = 1, page_size: int = 20):
        return self.list(page=page, page_size=page_size, workflow_id=workflow_id)


class WorkflowStepRunRepository(BaseRepository[WorkflowStepRun]):
    model = WorkflowStepRun

    def list_for_run(self, workflow_run_id: str) -> list[WorkflowStepRun]:
        stmt = (
            select(WorkflowStepRun)
            .where(WorkflowStepRun.workflow_run_id == workflow_run_id)
            .order_by(WorkflowStepRun.step_index)
        )
        return list(self.db.scalars(stmt).all())
