from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# Deliberately small: three built-in actions cover the common "automate a
# notification" cases without introducing an arbitrary-code or outbound-HTTP
# step type (an unrestricted webhook step is a natural next addition, but
# needs an allowlist/SSRF story before it belongs here).
StepType = Literal["send_notification", "notify_role", "send_email"]


class WorkflowStepDef(BaseModel):
    name: str
    type: StepType
    config: dict[str, Any] = Field(default_factory=dict)


class WorkflowCreate(BaseModel):
    name: str
    description: str | None = None
    trigger_type: Literal["manual", "scheduled", "event"] = "manual"
    schedule_cron: str | None = None
    is_active: bool = True
    steps: list[WorkflowStepDef] = Field(default_factory=list)


class WorkflowUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    steps: list[WorkflowStepDef] | None = None


class WorkflowRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None
    trigger_type: str
    schedule_cron: str | None
    is_active: bool
    steps: list[dict]
    created_at: datetime
    updated_at: datetime


class WorkflowStepRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    step_index: int
    step_name: str
    step_type: str
    status: str
    output: dict | None
    error: str | None
    started_at: datetime | None
    finished_at: datetime | None


class WorkflowRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    workflow_id: str
    status: str
    triggered_by: str | None
    started_at: datetime | None
    finished_at: datetime | None
    error: str | None
    created_at: datetime


class WorkflowRunDetail(WorkflowRunRead):
    step_runs: list[WorkflowStepRunRead]
