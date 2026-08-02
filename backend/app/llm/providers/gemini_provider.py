from __future__ import annotations

import json
from collections.abc import Iterator

import httpx

from app.core.config import settings
from app.llm.base import LLMMessage, LLMProvider, LLMResult
from app.llm.errors import LLMConfigError, LLMProviderError

_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"


class GeminiProvider(LLMProvider):
    name = "gemini"

    def _key(self) -> str:
        if not settings.GEMINI_API_KEY:
            raise LLMConfigError("GEMINI_API_KEY is not configured.")
        return settings.GEMINI_API_KEY

    @staticmethod
    def _split(messages: list[LLMMessage]) -> tuple[str | None, list[dict]]:
        system = "\n".join(m.content for m in messages if m.role == "system") or None
        contents = [
            {"role": "model" if m.role == "assistant" else "user", "parts": [{"text": m.content}]}
            for m in messages
            if m.role != "system"
        ]
        return system, contents

    def _payload(self, messages: list[LLMMessage], temperature: float, max_tokens: int) -> dict:
        system, contents = self._split(messages)
        payload: dict = {
            "contents": contents,
            "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
        }
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        return payload

    def complete(self, messages, model, *, temperature=0.3, max_tokens=1024) -> LLMResult:
        url = f"{_BASE_URL}/{model}:generateContent?key={self._key()}"
        payload = self._payload(messages, temperature, max_tokens)
        try:
            resp = httpx.post(url, json=payload, timeout=settings.LLM_REQUEST_TIMEOUT_SECONDS)
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise LLMProviderError(f"Gemini request failed: {exc}") from exc

        data = resp.json()
        content = data["candidates"][0]["content"]["parts"][0]["text"]
        return LLMResult(content=content, provider=self.name, model=model, raw=data)

    def stream(self, messages, model, *, temperature=0.3, max_tokens=1024) -> Iterator[str]:
        url = f"{_BASE_URL}/{model}:streamGenerateContent?alt=sse&key={self._key()}"
        payload = self._payload(messages, temperature, max_tokens)
        try:
            with httpx.stream(
                "POST", url, json=payload, timeout=settings.LLM_REQUEST_TIMEOUT_SECONDS
            ) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line or not line.startswith("data:"):
                        continue
                    chunk = json.loads(line[len("data:") :].strip())
                    try:
                        text = chunk["candidates"][0]["content"]["parts"][0]["text"]
                    except (KeyError, IndexError):
                        continue
                    if text:
                        yield text
        except httpx.HTTPError as exc:
            raise LLMProviderError(f"Gemini stream failed: {exc}") from exc
