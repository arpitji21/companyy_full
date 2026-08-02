from tests.conftest import auth_headers


def test_ceo_dashboard_success_for_ceo_role(client, db_session):
    headers = auth_headers(client, db_session, "founder2@larkai.test", role_name="CEO")

    resp = client.get("/api/ceo/dashboard", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert "company_health_score" in body
    assert "risk_score" in body
    assert "health_score_breakdown" in body
    assert "risk_score_breakdown" in body
    # Actual pending approvals the CEO can act on directly from the
    # dashboard (see CEODashboard.action_items in app/schemas/ceo.py).
    assert isinstance(body.get("action_items"), list)


def test_ceo_dashboard_reflects_pending_approvals(client, db_session):
    headers = auth_headers(client, db_session, "founder3@larkai.test", role_name="CEO")
    client.post("/api/approvals", json={"title": "New vendor contract", "amount": "5000.00"}, headers=headers)

    resp = client.get("/api/ceo/dashboard", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["pending_approvals"] >= 1
