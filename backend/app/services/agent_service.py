from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy import select

from app.agents.context import build_context
from app.agents.prompts import get_system_prompt
from app.core.exceptions import NotFoundError
from app.llm.base import LLMMessage
from app.llm.errors import LLMConfigError, LLMProviderError
from app.llm.factory import get_provider, resolve_model
from app.models.agent import AgentConversation, AgentMessage, AIAgent
from app.models.department import Department
from app.repositories.agent_repository import (
    AgentConversationRepository,
    AgentMessageRepository,
    AIAgentRepository,
)
from app.schemas.agent import AIAgentCreate, AIAgentUpdate

# Sliding window of prior turns fed back into the prompt as memory. Keeps
# token usage bounded without a separate summarization pass — bump this
# (or add real summarization) if conversations regularly run long.
MAX_HISTORY_MESSAGES = 20

# A control-line prefix used internally between the service and the SSE
# route to signal "here's the conversation id" before any text deltas.
# Never reaches the model or the persisted message content.
_CONVERSATION_ID_MARKER = "__conversation_id__:"


class AgentService:
    def __init__(self, db):
        self.db = db
        self.agents = AIAgentRepository(db)
        self.conversations = AgentConversationRepository(db)
        self.messages = AgentMessageRepository(db)

    # ------------------------------------------------------------------
    # Agents (admin/CEO configuration of which provider/model/prompt each
    # department copilot uses)
    # ------------------------------------------------------------------
    def list_agents(self) -> list[AIAgent]:
        return self.agents.get_active()

    def get_agent(self, agent_id: str) -> AIAgent:
        agent = self.agents.get(agent_id)
        if not agent:
            raise NotFoundError("AI agent not found.")
        return agent

    def create_agent(self, data: AIAgentCreate) -> AIAgent:
        model_name = data.model_name or resolve_model(data.provider, None)
        agent = AIAgent(
            name=data.name,
            department_id=data.department_id,
            provider=data.provider,
            model_name=model_name,
            system_prompt=data.system_prompt,
        )
        return self.agents.create(agent)

    def update_agent(self, agent_id: str, data: AIAgentUpdate) -> AIAgent:
        agent = self.get_agent(agent_id)
        return self.agents.update(agent, data.model_dump(exclude_unset=True))

    def get_or_create_default_agent(self, department_slug: str | None) -> AIAgent:
        """Falls back to a virtual (not-yet-persisted) agent if nobody has
        configured one for this department yet, so /api/chat always works
        even before an admin sets up agents via /api/agents. Persisted
        lazily — see `_persist_agent_if_needed` — only once it's actually
        used in a conversation."""
        dept = None
        if department_slug:
            dept = self.db.scalar(select(Department).where(Department.slug == department_slug.lower()))

        agent = self.agents.get_by_department(dept.id) if dept else None
        if agent:
            return agent

        default_provider = "openai"
        return AIAgent(
            name=f"{(department_slug or 'General').title()} Agent",
            department_id=dept.id if dept else None,
            provider=default_provider,
            model_name=resolve_model(default_provider, None),
            system_prompt=None,
            is_active=True,
        )

    # ------------------------------------------------------------------
    # Conversations
    # ------------------------------------------------------------------
    def create_conversation(self, agent_id: str, user_id: str, title: str | None = None) -> AgentConversation:
        agent = self.get_agent(agent_id)
        conv = AgentConversation(agent_id=agent.id, user_id=user_id, title=title)
        return self.conversations.create(conv)

    def list_conversations(self, user_id: str, agent_id: str | None = None) -> list[AgentConversation]:
        return self.conversations.list_for_user(user_id, agent_id)

    def get_conversation(self, conversation_id: str, user_id: str) -> AgentConversation:
        conv = self.conversations.get(conversation_id)
        if not conv or conv.user_id != user_id:
            raise NotFoundError("Conversation not found.")
        return conv

    def get_messages(self, conversation_id: str, user_id: str) -> list[AgentMessage]:
        self.get_conversation(conversation_id, user_id)  # ownership check
        return self.messages.list_for_conversation(conversation_id)

    # ------------------------------------------------------------------
    # Chat — non-streaming
    # ------------------------------------------------------------------
    def send_message(
        self,
        *,
        user_id: str,
        message: str,
        agent_id: str | None = None,
        conversation_id: str | None = None,
        department_slug: str | None = None,
        provider_override: str | None = None,
        model_override: str | None = None,
    ) -> tuple[AgentConversation, AgentMessage]:
        conversation, agent = self._resolve(
            user_id=user_id,
            agent_id=agent_id,
            conversation_id=conversation_id,
            department_slug=department_slug,
            first_message=message,
        )
        dept_slug = department_slug or self._department_slug(agent)

        provider_name = provider_override or agent.provider
        model_name = resolve_model(provider_name, model_override or agent.model_name)

        prompt = self._build_prompt(agent, conversation.id, dept_slug, message)
        self._save_message(conversation.id, "user", message)

        try:
            provider = get_provider(provider_name)
            result = provider.complete(prompt, model_name)
            content = result.content
        except (LLMConfigError, LLMProviderError) as exc:
            content = self._fallback_answer(str(exc))

        assistant_msg = self._save_message(conversation.id, "assistant", content)
        return conversation, assistant_msg

    # ------------------------------------------------------------------
    # Chat — streaming (SSE)
    # ------------------------------------------------------------------
    def stream_message(
        self,
        *,
        user_id: str,
        message: str,
        agent_id: str | None = None,
        conversation_id: str | None = None,
        department_slug: str | None = None,
        provider_override: str | None = None,
        model_override: str | None = None,
    ) -> Iterator[str]:
        """Yields text deltas as they arrive from the provider, then
        persists the full assistant message once the stream completes.
        The very first yielded item is a `__conversation_id__:<id>`
        control line — the API route turns that into an SSE
        `event: conversation` frame before any `event: delta` frames."""
        conversation, agent = self._resolve(
            user_id=user_id,
            agent_id=agent_id,
            conversation_id=conversation_id,
            department_slug=department_slug,
            first_message=message,
        )
        dept_slug = department_slug or self._department_slug(agent)

        provider_name = provider_override or agent.provider
        model_name = resolve_model(provider_name, model_override or agent.model_name)

        prompt = self._build_prompt(agent, conversation.id, dept_slug, message)
        self._save_message(conversation.id, "user", message)

        yield f"{_CONVERSATION_ID_MARKER}{conversation.id}"

        collected: list[str] = []
        try:
            provider = get_provider(provider_name)
            for chunk in provider.stream(prompt, model_name):
                collected.append(chunk)
                yield chunk
        except (LLMConfigError, LLMProviderError) as exc:
            fallback = self._fallback_answer(str(exc))
            collected.append(fallback)
            yield fallback

        self._save_message(conversation.id, "assistant", "".join(collected))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _resolve(
        self,
        *,
        user_id: str,
        agent_id: str | None,
        conversation_id: str | None,
        department_slug: str | None,
        first_message: str,
    ) -> tuple[AgentConversation, AIAgent]:
        """Resolves (conversation, agent) for a chat turn.

        If `conversation_id` is given, the conversation's *own* agent is
        always used — an existing thread must stay associated with the
        agent it started with; `agent_id`/`department_slug` on later
        turns of the same conversation are ignored rather than silently
        rerouting an established thread to a different (possibly brand
        new) agent. Otherwise a fresh conversation is started against the
        agent resolved from `agent_id` (or `department_slug`, or a
        general default)."""
        if conversation_id:
            conversation = self.get_conversation(conversation_id, user_id)
            agent = self.get_agent(conversation.agent_id)
            return conversation, agent

        agent = self._resolve_agent(agent_id, department_slug)
        agent = self._persist_agent_if_needed(agent)
        title = (first_message[:60] + "…") if len(first_message) > 60 else first_message
        conversation = self.conversations.create(AgentConversation(agent_id=agent.id, user_id=user_id, title=title))
        return conversation, agent

    def _resolve_agent(self, agent_id: str | None, department_slug: str | None) -> AIAgent:
        if agent_id:
            return self.get_agent(agent_id)
        return self.get_or_create_default_agent(department_slug)

    def _persist_agent_if_needed(self, agent: AIAgent) -> AIAgent:
        """The default agent from get_or_create_default_agent isn't saved
        until it's actually used, so departments nobody ever chats with
        don't clutter the ai_agents table with unused rows."""
        if agent.id is None:
            self.db.add(agent)
            self.db.commit()
            self.db.refresh(agent)
        return agent

    def _department_slug(self, agent: AIAgent) -> str | None:
        if not agent.department_id:
            return None
        dept = self.db.get(Department, agent.department_id)
        return dept.slug if dept else None

    def _build_prompt(
        self, agent: AIAgent, conversation_id: str | None, department_slug: str | None, new_user_message: str
    ) -> list[LLMMessage]:
        system_prompt = get_system_prompt(department_slug, agent.system_prompt)
        context = build_context(department_slug, self.db)
        if context:
            system_prompt = f"{system_prompt}\n\n{context}"

        prompt = [LLMMessage(role="system", content=system_prompt)]

        if conversation_id:
            history = self.messages.list_for_conversation(conversation_id, limit=MAX_HISTORY_MESSAGES)
            prompt.extend(LLMMessage(role=m.role, content=m.content) for m in history if m.role in ("user", "assistant"))

        prompt.append(LLMMessage(role="user", content=new_user_message))
        return prompt

    def _save_message(self, conversation_id: str, role: str, content: str) -> AgentMessage:
        msg = AgentMessage(conversation_id=conversation_id, role=role, content=content)
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg

    @staticmethod
    def _fallback_answer(error: str) -> str:
        return (
            "I can't reach the configured AI provider right now "
            f"({error}). Once an API key is set in the environment for "
            "that provider, this agent will answer using live data."
        )
