from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.agent import (
    AgentConversationCreate,
    AgentConversationRead,
    AgentMessageRead,
    AIAgentCreate,
    AIAgentRead,
    AIAgentUpdate,
)
from app.services.agent_service import AgentService

router = APIRouter(prefix="/agents", tags=["AI Agents"])


@router.get("", response_model=list[AIAgentRead])
def list_agents(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return AgentService(db).list_agents()


@router.post("", response_model=AIAgentRead, status_code=201)
def create_agent(
    payload: AIAgentCreate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin")),
):
    return AgentService(db).create_agent(payload)


@router.get("/{agent_id}", response_model=AIAgentRead)
def get_agent(agent_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return AgentService(db).get_agent(agent_id)


@router.patch("/{agent_id}", response_model=AIAgentRead)
def update_agent(
    agent_id: str,
    payload: AIAgentUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin")),
):
    return AgentService(db).update_agent(agent_id, payload)


@router.post("/conversations", response_model=AgentConversationRead, status_code=201)
def create_conversation(
    payload: AgentConversationCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return AgentService(db).create_conversation(payload.agent_id, user.id, payload.title)


@router.get("/conversations", response_model=list[AgentConversationRead])
def list_conversations(
    agent_id: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return AgentService(db).list_conversations(user.id, agent_id)


@router.get("/conversations/{conversation_id}/messages", response_model=list[AgentMessageRead])
def get_conversation_messages(
    conversation_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    return AgentService(db).get_messages(conversation_id, user.id)
