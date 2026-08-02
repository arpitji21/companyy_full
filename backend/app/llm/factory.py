from __future__ import annotations

from app.llm.base import LLMProvider
from app.llm.errors import LLMConfigError
from app.llm.providers.claude_provider import ClaudeProvider
from app.llm.providers.gemini_provider import GeminiProvider
from app.llm.providers.ollama_provider import OllamaProvider
from app.llm.providers.openai_provider import OpenAIProvider

_PROVIDERS: dict[str, type[LLMProvider]] = {
    "openai": OpenAIProvider,
    "claude": ClaudeProvider,
    "gemini": GeminiProvider,
    "ollama": OllamaProvider,
}

# Used whenever an agent/request doesn't pin a specific model — this is the
# one place that knows what "the current best model" is for each provider,
# so upgrading a default never means touching route or service code.
_DEFAULT_MODELS: dict[str, str] = {
    "openai": "gpt-4o-mini",
    "claude": "claude-sonnet-4-6",
    "gemini": "gemini-2.0-flash",
    "ollama": "llama3.1",
}

SUPPORTED_PROVIDERS = tuple(_PROVIDERS)


def get_provider(name: str) -> LLMProvider:
    """Returns the provider implementation for `name`. Raises
    LLMConfigError for an unknown provider name (bad config, typo) —
    callers should treat this the same as a missing API key: a graceful
    fallback, not a 500."""
    key = (name or "").strip().lower()
    provider_cls = _PROVIDERS.get(key)
    if not provider_cls:
        raise LLMConfigError(f"Unknown LLM provider '{name}'. Supported providers: {', '.join(SUPPORTED_PROVIDERS)}.")
    return provider_cls()


def resolve_model(provider: str, requested_model: str | None) -> str:
    """Model-selection logic: explicit request wins, otherwise fall back to
    that provider's current default model."""
    if requested_model:
        return requested_model
    return _DEFAULT_MODELS.get((provider or "").strip().lower(), "")
