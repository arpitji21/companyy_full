from sqlalchemy import select

from app.models.agent import AgentConversation, AgentMessage, AIAgent
from app.repositories.base import BaseRepository


class AIAgentRepository(BaseRepository[AIAgent]):
    model = AIAgent

    def get_by_department(self, department_id: str) -> AIAgent | None:
        return self.db.scalar(
            select(AIAgent).where(AIAgent.department_id == department_id, AIAgent.is_active.is_(True))
        )

    def get_active(self) -> list[AIAgent]:
        return list(self.db.scalars(select(AIAgent).where(AIAgent.is_active.is_(True))).all())


class AgentConversationRepository(BaseRepository[AgentConversation]):
    model = AgentConversation

    def list_for_user(self, user_id: str, agent_id: str | None = None) -> list[AgentConversation]:
        stmt = select(AgentConversation).where(AgentConversation.user_id == user_id)
        if agent_id:
            stmt = stmt.where(AgentConversation.agent_id == agent_id)
        stmt = stmt.order_by(AgentConversation.created_at.desc())
        return list(self.db.scalars(stmt).all())


class AgentMessageRepository(BaseRepository[AgentMessage]):
    model = AgentMessage

    def list_for_conversation(self, conversation_id: str, limit: int = 50) -> list[AgentMessage]:
        stmt = (
            select(AgentMessage)
            .where(AgentMessage.conversation_id == conversation_id)
            .order_by(AgentMessage.created_at.asc())
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())
