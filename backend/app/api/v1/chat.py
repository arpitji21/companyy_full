import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.agents.brain import run_brain_query
from app.auth.dependencies import get_current_active_user
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.agent import (
    AgentMessageRead,
    BrainQueryRequest,
    BrainQueryResponse,
    ChatRequest,
    ChatResponse,
)
from app.services.agent_service import AgentService

router = APIRouter(prefix="/chat", tags=["Chat"])

_CONVERSATION_ID_MARKER = "__conversation_id__:"


@router.post("", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    """Single-shot (non-streaming) chat turn. Creates a new conversation if
    `conversation_id` is omitted. For token-by-token output use
    POST /api/chat/stream instead."""
    conversation, message = AgentService(db).send_message(
        user_id=user.id,
        message=payload.message,
        agent_id=payload.agent_id,
        conversation_id=payload.conversation_id,
        department_slug=payload.department_slug,
        provider_override=payload.provider,
        model_override=payload.model,
    )
    return ChatResponse(conversation_id=conversation.id, message=AgentMessageRead.model_validate(message))


@router.post("/stream")
def chat_stream(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    """Server-Sent Events stream of a chat turn.

    Frames emitted, in order:
      event: conversation  data: {"conversation_id": "..."}
      event: delta         data: {"text": "..."}         (repeated)
      event: done          data: {}
    """
    service = AgentService(db)

    def event_source():
        for chunk in service.stream_message(
            user_id=user.id,
            message=payload.message,
            agent_id=payload.agent_id,
            conversation_id=payload.conversation_id,
            department_slug=payload.department_slug,
            provider_override=payload.provider,
            model_override=payload.model,
        ):
            if chunk.startswith(_CONVERSATION_ID_MARKER):
                conv_id = chunk[len(_CONVERSATION_ID_MARKER) :]
                yield f"event: conversation\ndata: {json.dumps({'conversation_id': conv_id})}\n\n"
                continue
            yield f"event: delta\ndata: {json.dumps({'text': chunk})}\n\n"
        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(
        event_source(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/brain", response_model=BrainQueryResponse)
def brain_query(
    payload: BrainQueryRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    """The LarkAI Brain — routes a free-text question to one or more
    department agents (e.g. "show departments overspending" -> Finance)
    and combines their answers into a single response. Use this instead
    of /api/chat when the question isn't scoped to one department."""
    return run_brain_query(
        db,
        payload.query,
        provider_name=payload.provider or settings.DEFAULT_LLM_PROVIDER,
        model_name=payload.model,
    )
