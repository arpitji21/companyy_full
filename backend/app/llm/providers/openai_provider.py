from __future__ import annotations

import json
from collections.abc import Iterator

import httpx

from app.core.config import settings
from app.llm.base import LLMMessage, LLMProvider, LLMResult
from app.llm.errors import LLMConfigError, LLMProviderError

_API_URL = "https://api.openai.com/v1/chat/completions"


class OpenAIProvider(LLMProvider):
    name = "openai"

    def _headers(self) -> dict:
        if not settings.OPENAI_API_KEY:
            raise LLMConfigError("OPENAI_API_KEY is not configured.")
        return {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _payload(messages: list[LLMMessage], model: str, temperature: float, max_tokens: int, stream: bool) -> dict:
        return {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }

    def complete(self, messages, model, *, temperature=0.3, max_tokens=1024) -> LLMResult:
        payload = self._payload(messages, model, temperature, max_tokens, stream=False)
        try:
            resp = httpx.post(
                _API_URL, headers=self._headers(), json=payload, timeout=settings.LLM_REQUEST_TIMEOUT_SECONDS
            )
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise LLMProviderError(f"OpenAI request failed: {exc}") from exc

        data = resp.json()
        content = data["choices"][0]["message"]["content"]
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
                    data = line[len("data:") :].strip()
                    if data == "[DONE]":
                        break
                    chunk = json.loads(data)
                    delta = chunk["choices"][0].get("delta", {})
                    text = delta.get("content")
                    if text:
                        yield text
        except httpx.HTTPError as exc:
            raise LLMProviderError(f"OpenAI stream failed: {exc}") from exc
