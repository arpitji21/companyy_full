from tests.conftest import auth_headers


def test_create_and_list_tenders(client, db_session):
    headers = auth_headers(client, db_session, "tender-lead@larkai.test", role_name="Manager")

    create_resp = client.post(
        "/api/tender/tenders",
        json={"title": "Government hospital contract", "client_segment": "public", "bid_value": "1500000.00"},
        headers=headers,
    )
    assert create_resp.status_code == 201
    tender = create_resp.json()
    assert tender["title"] == "Government hospital contract"
    assert tender["status"] == "draft"

    listing = client.get("/api/tender/tenders?client_segment=public", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["total"] >= 1

    get_resp = client.get(f"/api/tender/tenders/{tender['id']}", headers=headers)
    assert get_resp.status_code == 200


def test_update_tender_outcome(client, db_session):
    headers = auth_headers(client, db_session, "tender-lead2@larkai.test", role_name="Manager")
    tender = client.post("/api/tender/tenders", json={"title": "Private clinic deal"}, headers=headers).json()

    update_resp = client.patch(
        f"/api/tender/tenders/{tender['id']}",
        json={"status": "won", "outcome_date": "2026-07-20"},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "won"


def test_summary_computes_win_rate(client, db_session):
    headers = auth_headers(client, db_session, "tender-lead3@larkai.test", role_name="Manager")
    won = client.post("/api/tender/tenders", json={"title": "Won deal"}, headers=headers).json()
    client.patch(f"/api/tender/tenders/{won['id']}", json={"status": "won"}, headers=headers)

    summary = client.get("/api/tender/summary", headers=headers)
    assert summary.status_code == 200
    assert summary.json()["won"] >= 1


def test_creating_tender_requires_elevated_role(client, db_session):
    headers = auth_headers(client, db_session, "plain-user@larkai.test")
    resp = client.post("/api/tender/tenders", json={"title": "Should be denied"}, headers=headers)
    assert resp.status_code == 403
