from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class AIAgent(UUIDPKMixin, TimestampMixin, Base):
    """One row per department copilot (CEO Agent, Finance Agent, ...)."""
    __tablename__ = "ai_agents"

    name: Mapped[str] = mapped_column(String(100))  # "Finance Agent"
    department_id: Mapped[str | None] = mapped_column(ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    provider: Mapped[str] = mapped_column(String(30), default="openai")  # openai, claude, gemini, ollama
    model_name: Mapped[str] = mapped_column(String(100), default="gpt-4o-mini")
    system_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    conversations: Mapped[list["AgentConversation"]] = relationship(back_populates="agent")


class AgentConversation(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "agent_conversations"

    agent_id: Mapped[str] = mapped_column(ForeignKey("ai_agents.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)

    agent: Mapped["AIAgent"] = relationship(back_populates="conversations")
    messages: Mapped[list["AgentMessage"]] = relationship(back_populates="conversation", cascade="all, delete-orphan")


class AgentMessage(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "agent_messages"

    conversation_id: Mapped[str] = mapped_column(ForeignKey("agent_conversations.id", ondelete="CASCADE"), index=True)
    role: Mapped[str] = mapped_column(String(20))  # user, assistant, system, tool
    content: Mapped[str] = mapped_column(Text)

    conversation: Mapped["AgentConversation"] = relationship(back_populates="messages")
