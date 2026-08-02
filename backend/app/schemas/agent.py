from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.llm.factory import SUPPORTED_PROVIDERS


class AIAgentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: str
    name: str
    department_id: str | None
    provider: str
    model_name: str
    system_prompt: str | None
    is_active: bool


class AIAgentCreate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    name: str
    department_id: str | None = None
    provider: str = "openai"
    model_name: str | None = None  # falls back to that provider's default
    system_prompt: str | None = None


class AIAgentUpdate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    name: str | None = None
    provider: str | None = None
    model_name: str | None = None
    system_prompt: str | None = None
    is_active: bool | None = None


class AgentConversationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    agent_id: str
    user_id: str
    title: str | None
    created_at: datetime


class AgentConversationCreate(BaseModel):
    agent_id: str
    title: str | None = None


class AgentMessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime


class ChatRequest(BaseModel):
    message: str
    agent_id: str | None = None  # if omitted, resolved from department_slug (or a general default)
    conversation_id: str | None = None  # if omitted, a new conversation is started
    department_slug: str | None = None
    provider: str | None = None  # overrides the agent's configured provider for this turn
    model: str | None = None  # overrides the agent's configured model for this turn


class ChatResponse(BaseModel):
    conversation_id: str
    message: AgentMessageRead


class BrainQueryRequest(BaseModel):
    query: str
    provider: str | None = None
    model: str | None = None


class BrainDepartmentResult(BaseModel):
    department: str
    answer: str


class BrainQueryResponse(BaseModel):
    query: str
    routed_departments: list[str]
    results: list[BrainDepartmentResult]
    combined_answer: str


__all__ = [
    "AIAgentRead",
    "AIAgentCreate",
    "AIAgentUpdate",
    "AgentConversationRead",
    "AgentConversationCreate",
    "AgentMessageRead",
    "ChatRequest",
    "ChatResponse",
    "BrainQueryRequest",
    "BrainDepartmentResult",
    "BrainQueryResponse",
    "SUPPORTED_PROVIDERS",
]
