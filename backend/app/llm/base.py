from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass, field


@dataclass
class LLMMessage:
    """One turn in a conversation, provider-agnostic."""

    role: str  # "system" | "user" | "assistant"
    content: str


@dataclass
class LLMResult:
    content: str
    provider: str
    model: str
    raw: dict = field(default_factory=dict)


class LLMProvider(ABC):
    """Every LLM backend (OpenAI, Claude, Gemini, Ollama) implements this
    single interface. Route and service code only ever talks to
    `LLMProvider` — swapping providers means adding a class here and a
    line in `app/llm/factory.py`, never touching `app/api` or
    `app/services`.
    """

    name: str

    @abstractmethod
    def complete(
        self,
        messages: list[LLMMessage],
        model: str,
        *,
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> LLMResult:
        """Single request/response call — used for non-streaming chat and
        for the Brain's per-department and combine-step calls."""

    @abstractmethod
    def stream(
        self,
        messages: list[LLMMessage],
        model: str,
        *,
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> Iterator[str]:
        """Yields text deltas as they arrive, for the SSE /api/chat/stream
        endpoint. Implementations should yield plain text chunks only —
        no provider-specific framing leaks past this interface."""
