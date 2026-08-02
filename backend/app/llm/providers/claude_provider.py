from __future__ import annotations

import json
from collections.abc import Iterator

import httpx

from app.core.config import settings
from app.llm.base import LLMMessage, LLMProvider, LLMResult
from app.llm.errors import LLMConfigError, LLMProviderError

_API_URL = "https://api.anthropic.com/v1/messages"
_API_VERSION = "2023-06-01"


class ClaudeProvider(LLMProvider):
    name = "claude"

    def _headers(self) -> dict:
        if not settings.ANTHROPIC_API_KEY:
            raise LLMConfigError("ANTHROPIC_API_KEY is not configured.")
        return {
            "x-api-key": settings.ANTHROPIC_API_KEY,
            "anthropic-version": _API_VERSION,
            "Content-Type": "application/json",
        }

    @staticmethod
    def _split(messages: list[LLMMessage]) -> tuple[str | None, list[dict]]:
        """Anthropic takes `system` as a separate top-level field rather
        than a message with role='system'."""
        system = "\n".join(m.content for m in messages if m.role == "system") or None
        convo = [{"role": m.role, "content": m.content} for m in messages if m.role != "system"]
        return system, convo

    def _payload(self, messages: list[LLMMessage], model: str, temperature: float, max_tokens: int, stream: bool) -> dict:
        system, convo = self._split(messages)
        payload: dict = {
            "model": model,
            "messages": convo,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream,
        }
        if system:
            payload["system"] = system
        return payload

    def complete(self, messages, model, *, temperature=0.3, max_tokens=1024) -> LLMResult:
        payload = self._payload(messages, model, temperature, max_tokens, stream=False)
        try:
            resp = httpx.post(
                _API_URL, headers=self._headers(), json=payload, timeout=settings.LLM_REQUEST_TIMEOUT_SECONDS
            )
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise LLMProviderError(f"Claude request failed: {exc}") from exc

        data = resp.json()
        content = "".join(block.get("text", "") for block in data.get("content", []))
        return LLMResult(content=content, provider=self.name, model=model, raw=data)

    def stream(self, messages, model, *, temperature=0.3, max_tokens=1024) -> Iterator[str]:
        payload = self._payload(messages, model, temperature, max_tokens, stream=True)
        try:
            with httpx.stream(
                "POST", _API_URL, headers=self._headers(), json=payload, timeout=settings.LLM_REQUEST_TIMEOUT_SECONDS
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line or not line.startswith("data:"):
                        continue
                    event = json.loads(line[len("data:") :].strip())
                    event_type = event.get("type")
                    if event_type == "content_block_delta":
                        text = event.get("delta", {}).get("text")
                        if text:
                            yield text
                    elif event_type == "message_stop":
                        break
        except httpx.HTTPError as exc:
            raise LLMProviderError(f"Claude stream failed: {exc}") from exc
