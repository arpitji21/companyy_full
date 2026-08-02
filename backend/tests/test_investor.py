from tests.conftest import auth_headers


def test_create_and_list_rounds(client, db_session):
    headers = auth_headers(client, db_session, "investor-lead@larkai.test", role_name="Investor")

    create_resp = client.post(
        "/api/investor/rounds",
        json={"round_name": "Series A", "amount_raised": "5000000.00", "status": "closed"},
        headers=headers,
    )
    assert create_resp.status_code == 201
    round_ = create_resp.json()
    assert round_["round_name"] == "Series A"

    listing = client.get("/api/investor/rounds?status=closed", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["total"] >= 1

    get_resp = client.get(f"/api/investor/rounds/{round_['id']}", headers=headers)
    assert get_resp.status_code == 200


def test_update_round(client, db_session):
    headers = auth_headers(client, db_session, "investor-lead2@larkai.test", role_name="Investor")
    round_ = client.post("/api/investor/rounds", json={"round_name": "Series B"}, headers=headers).json()

    update_resp = client.patch(
        f"/api/investor/rounds/{round_['id']}",
        json={"status": "closed", "amount_raised": "12000000.00"},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "closed"


def test_create_and_list_updates(client, db_session):
    headers = auth_headers(client, db_session, "investor-lead3@larkai.test", role_name="Investor")

    update_resp = client.post(
        "/api/investor/updates",
        json={"title": "Q2 investor letter", "update_type": "investor_update"},
        headers=headers,
    )
    assert update_resp.status_code == 201

    listing = client.get("/api/investor/updates", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["total"] >= 1


def test_summary_totals_raised(client, db_session):
    headers = auth_headers(client, db_session, "investor-lead4@larkai.test", role_name="Investor")
    client.post(
        "/api/investor/rounds",
        json={"round_name": "Seed", "amount_raised": "500000.00", "status": "closed"},
        headers=headers,
    )

    summary = client.get("/api/investor/summary", headers=headers)
    assert summary.status_code == 200
    assert float(summary.json()["total_raised"]) >= 500000.0


def test_creating_round_requires_elevated_role(client, db_session):
    headers = auth_headers(client, db_session, "plain-user@larkai.test")
    resp = client.post("/api/investor/rounds", json={"round_name": "Should be denied"}, headers=headers)
    assert resp.status_code == 403
