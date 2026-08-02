class LLMConfigError(Exception):
    """Raised when a provider is selected but isn't configured (e.g. missing
    API key). Caught by the agent/brain layer and turned into a graceful,
    user-visible fallback message rather than a 500."""


class LLMProviderError(Exception):
    """Raised when the upstream provider call itself fails (network error,
    non-2xx response, malformed payload, etc.)."""
