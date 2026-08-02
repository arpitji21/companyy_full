from __future__ import annotations

import json
from collections.abc import Iterator

import httpx

from app.core.config import settings
from app.llm.base import LLMMessage, LLMProvider, LLMResult
from app.llm.errors import LLMProviderError


class OllamaProvider(LLMProvider):
    """Local model runner — no API key required, just a reachable
    OLLAMA_BASE_URL (defaults to http://localhost:11434)."""

    name = "ollama"

    def _url(self) -> str:
        return f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/chat"

    @staticmethod
    def _payload(messages: list[LLMMessage], model: str, temperature: float, stream: bool) -> dict:
        return {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": stream,
            "options": {"temperature": temperature},
        }

    def complete(self, messages, model, *, temperature=0.3, max_tokens=1024) -> LLMResult:
        payload = self._payload(messages, model, temperature, stream=False)
        try:
            resp = httpx.post(self._url(), json=payload, timeout=settings.LLM_REQUEST_TIMEOUT_SECONDS)
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise LLMProviderError(f"Ollama request failed: {exc}") from exc

        data = resp.json()
        content = data.get("message", {}).get("content", "")
        return LLMResult(content=content, provider=self.name, model=model, raw=data)

    def stream(self, messages, model, *, temperature=0.3, max_tokens=1024) -> Iterator[str]:
        payload = self._payload(messages, model, temperature, stream=True)
        try:
            with httpx.stream(
                "POST", self._url(), json=payload, timeout=settings.LLM_REQUEST_TIMEOUT_SECONDS
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    text = chunk.get("message", {}).get("content")
                    if text:
                        yield text
                    if chunk.get("done"):
                        break
        except httpx.HTTPError as exc:
            raise LLMProviderError(f"Ollama stream failed: {exc}") from exc
