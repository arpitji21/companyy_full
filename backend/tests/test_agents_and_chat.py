from app.agents.brain import route_query
from tests.conftest import auth_headers

FALLBACK_PHRASE = "can't reach the configured AI provider"


def test_route_query_matches_department_keywords():
    assert "finance" in route_query("why are we overspending our budget this quarter")
    assert "hr" in route_query("what's our current headcount and attrition")
    assert "sales" in route_query("show me the deal pipeline forecast")


def test_route_query_falls_back_to_ceo_for_unmatched_text():
    assert route_query("tell me a joke about the weather") == ["ceo"]


def test_create_agent_requires_elevated_role(client, db_session):
    headers = auth_headers(client, db_session, "plain-user@larkai.test")
    resp = client.post("/api/agents", json={"name": "Finance Copilot"}, headers=headers)
    assert resp.status_code == 403


def test_create_list_and_get_agent(client, db_session):
    headers = auth_headers(client, db_session, "admin@larkai.test", role_name="Admin")

    create_resp = client.post(
        "/api/agents", json={"name": "Finance Copilot", "provider": "openai"}, headers=headers
    )
    assert create_resp.status_code == 201
    agent = create_resp.json()
    assert agent["model_name"]  # filled in from the provider's default

    listing = client.get("/api/agents", headers=headers)
    assert listing.status_code == 200
    assert any(a["id"] == agent["id"] for a in listing.json())

    get_resp = client.get(f"/api/agents/{agent['id']}", headers=headers)
    assert get_resp.status_code == 200


def test_chat_without_llm_key_returns_graceful_fallback(client, db_session):
    """No LLM provider is configured in tests, so the assistant's reply
    should be the documented fallback message, not a crash — this proves
    the "no API key configured" path actually degrades gracefully rather
    than just being a docstring's promise."""
    headers = auth_headers(client, db_session, "chat-user@larkai.test")

    resp = client.post("/api/chat", json={"message": "How is finance doing this month?"}, headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["conversation_id"]
    assert body["message"]["role"] == "assistant"
    assert FALLBACK_PHRASE in body["message"]["content"]


def test_chat_follow_up_reuses_same_conversation_and_agent(client, db_session):
    headers = auth_headers(client, db_session, "chat-user2@larkai.test")

    first = client.post("/api/chat", json={"message": "First message"}, headers=headers).json()
    conversation_id = first["conversation_id"]

    second = client.post(
        "/api/chat",
        json={"message": "Second message", "conversation_id": conversation_id},
        headers=headers,
    ).json()
    assert second["conversation_id"] == conversation_id

    messages = client.get(f"/api/agents/conversations/{conversation_id}/messages", headers=headers)
    assert messages.status_code == 200
    roles = [m["role"] for m in messages.json()]
    assert roles == ["user", "assistant", "user", "assistant"]


def test_conversation_belongs_to_its_owner_only(client, db_session):
    owner_headers = auth_headers(client, db_session, "owner@larkai.test")
    other_headers = auth_headers(client, db_session, "other@larkai.test")

    chat_resp = client.post("/api/chat", json={"message": "Private question"}, headers=owner_headers).json()
    conversation_id = chat_resp["conversation_id"]

    resp = client.get(f"/api/agents/conversations/{conversation_id}/messages", headers=other_headers)
    assert resp.status_code == 404


def test_chat_stream_emits_sse_frames(client, db_session):
    headers = auth_headers(client, db_session, "stream-user@larkai.test")

    resp = client.post("/api/chat/stream", json={"message": "Stream this please"}, headers=headers)
    assert resp.status_code == 200
    body = resp.text
    assert "event: conversation" in body
    assert "event: done" in body
    assert FALLBACK_PHRASE in body


def test_brain_query_routes_and_answers(client, db_session):
    headers = auth_headers(client, db_session, "brain-user@larkai.test")

    resp = client.post("/api/chat/brain", json={"query": "why is our burn rate so high"}, headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert "finance" in body["routed_departments"]
    assert len(body["results"]) == len(body["routed_departments"])
    assert body["combined_answer"]
