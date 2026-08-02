"""The LarkAI Brain: takes one free-text query (e.g. "show departments
overspending") and figures out which department agent(s) should answer it,
asks each of them (grounded with their own live data snapshot), then
combines the answers into one response.

Routing is currently simple keyword matching rather than an LLM classifier
— intentionally: it's fast, free, deterministic, and easy to extend. Swap
`route_query` for an LLM-based router later without touching anything
that calls `run_brain_query`.
"""

from __future__ import annotations

from app.agents.context import build_context
from app.agents.prompts import DEPARTMENT_PROMPTS, DEFAULT_PROMPT
from app.llm.base import LLMMessage
from app.llm.errors import LLMConfigError, LLMProviderError
from app.llm.factory import get_provider, resolve_model

# department slug -> keywords that route a query to it. A query can match
# more than one department (e.g. "overspending" could hit both finance and
# supplychain), and the Brain will ask all matches and combine them.
_ROUTING_KEYWORDS: dict[str, list[str]] = {
    "finance": ["budget", "revenue", "expense", "cash", "spend", "overspend", "burn rate", "cost", "profit", "financ"],
    "hr": ["employee", "headcount", "hiring", "leave", "attrition", "payroll", "recruit", "onboarding", "staff"],
    "sales": ["deal", "pipeline", "customer", "lead", "quota", "forecast", "won", "lost"],
    "marketing": ["campaign", "channel", "ctr", "impression", "conversion", "brand"],
    "manufacturing": ["batch", "production", "yield", "downtime", "factory", "manufactur"],
    "quality": ["defect", "quality", "inspection", "pass rate"],
    "compliance": ["compliance", "audit", "regulation", "violation"],
    "supplychain": ["inventory", "vendor", "supplier", "stock", "shipment", "reorder"],
    "projects": ["project", "task", "deadline", "milestone", "overdue"],
}


def route_query(query: str) -> list[str]:
    """Returns the department slugs relevant to `query`. Never returns
    empty — falls back to ['ceo'] (the cross-department agent) so the
    Brain always has something to answer from."""
    q = query.lower()
    matched = [dept for dept, keywords in _ROUTING_KEYWORDS.items() if any(kw in q for kw in keywords)]
    return matched or ["ceo"]


def _ask_department(db, department_slug: str, query: str, provider_name: str, model_name: str) -> str:
    system_prompt = DEPARTMENT_PROMPTS.get(department_slug, DEFAULT_PROMPT)
    context = build_context(department_slug, db)
    full_system = f"{system_prompt}\n\n{context}" if context else system_prompt

    messages = [
        LLMMessage(role="system", content=full_system),
        LLMMessage(role="user", content=query),
    ]

    try:
        provider = get_provider(provider_name)
        result = provider.complete(messages, model_name)
        return result.content
    except (LLMConfigError, LLMProviderError) as exc:
        # No LLM reachable — the live snapshot alone is still a real,
        # useful answer (e.g. actual overspend numbers), just unwritten.
        return context or f"({department_slug} agent unavailable: {exc})"


def _combine(query: str, results: list[dict], provider_name: str, model_name: str) -> str:
    if len(results) == 1:
        return results[0]["answer"]

    joined = "\n\n".join(f"[{r['department']}]\n{r['answer']}" for r in results)
    messages = [
        LLMMessage(
            role="system",
            content=(
                "You are the LarkAI Brain. Combine the answers below from "
                "multiple department agents into one concise, "
                "non-repetitive answer to the original question. "
                "Attribute specific figures to their department."
            ),
        ),
        LLMMessage(role="user", content=f"Original question: {query}\n\nDepartment answers:\n{joined}"),
    ]
    try:
        provider = get_provider(provider_name)
        result = provider.complete(messages, model_name)
        return result.content
    except (LLMConfigError, LLMProviderError):
        # No LLM available to synthesize — the concatenated per-department
        # answers are still complete and readable on their own.
        return joined


def run_brain_query(db, query: str, *, provider_name: str = "openai", model_name: str | None = None) -> dict:
    resolved_model = resolve_model(provider_name, model_name)
    departments = route_query(query)

    results = [
        {"department": dept, "answer": _ask_department(db, dept, query, provider_name, resolved_model)}
        for dept in departments
    ]

    combined = _combine(query, results, provider_name, resolved_model)

    return {
        "query": query,
        "routed_departments": departments,
        "results": results,
        "combined_answer": combined,
    }
