from tests.conftest import auth_headers


def test_summary_blends_departments(client, db_session):
    headers = auth_headers(client, db_session, "analytics-lead@larkai.test")

    summary = client.get("/api/analytics/summary", headers=headers)
    assert summary.status_code == 200
    body = summary.json()
    assert "total_revenue" in body
    assert "snapshots" in body
    assert isinstance(body["snapshots"], list)


def test_create_report_returns_immediately_pending_s3_key(client, db_session):
    """Report generation happens in the background (Celery) — the row
    comes back right away with s3_key still unset. See
    app/tasks/reports.py, which fills it in once the worker runs."""
    headers = auth_headers(client, db_session, "analytics-lead2@larkai.test", role_name="Manager")

    create_resp = client.post(
        "/api/analytics/reports",
        json={"title": "Q2 board report", "report_type": "board"},
        headers=headers,
    )
    assert create_resp.status_code == 201
    report = create_resp.json()
    assert report["title"] == "Q2 board report"
    assert report["s3_key"] is None

    get_resp = client.get(f"/api/analytics/reports/{report['id']}", headers=headers)
    assert get_resp.status_code == 200

    listing = client.get("/api/analytics/reports?report_type=board", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["total"] >= 1


def test_creating_report_requires_elevated_role(client, db_session):
    headers = auth_headers(client, db_session, "plain-user@larkai.test")
    resp = client.post("/api/analytics/reports", json={"title": "Should be denied"}, headers=headers)
    assert resp.status_code == 403
