from tests.conftest import auth_headers


def test_create_and_list_trials(client, db_session):
    headers = auth_headers(client, db_session, "clinical-lead@larkai.test", role_name="Manager")

    create_resp = client.post(
        "/api/clinical/trials",
        json={"title": "Phase II efficacy study", "phase": "II", "target_enrollment": 200},
        headers=headers,
    )
    assert create_resp.status_code == 201
    trial = create_resp.json()
    assert trial["phase"] == "II"
    assert trial["status"] == "planning"

    listing = client.get("/api/clinical/trials?phase=II", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["total"] >= 1

    get_resp = client.get(f"/api/clinical/trials/{trial['id']}", headers=headers)
    assert get_resp.status_code == 200


def test_update_trial_enrollment(client, db_session):
    headers = auth_headers(client, db_session, "clinical-lead2@larkai.test", role_name="Manager")
    trial = client.post(
        "/api/clinical/trials", json={"title": "Phase I safety study", "phase": "I"}, headers=headers
    ).json()

    update_resp = client.patch(
        f"/api/clinical/trials/{trial['id']}",
        json={"status": "active", "actual_enrollment": 50},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["actual_enrollment"] == 50


def test_create_and_list_events(client, db_session):
    headers = auth_headers(client, db_session, "clinical-lead3@larkai.test", role_name="Manager")
    trial = client.post(
        "/api/clinical/trials", json={"title": "Phase III trial", "phase": "III"}, headers=headers
    ).json()

    event_resp = client.post(
        "/api/clinical/events",
        json={
            "trial_id": trial["id"],
            "event_type": "adverse_event",
            "severity": "moderate",
            "reported_date": "2026-07-15",
        },
        headers=headers,
    )
    assert event_resp.status_code == 201

    listing = client.get(f"/api/clinical/events?trial_id={trial['id']}", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["total"] >= 1


def test_summary_counts_trials_and_events(client, db_session):
    headers = auth_headers(client, db_session, "clinical-lead4@larkai.test", role_name="Manager")
    client.post("/api/clinical/trials", json={"title": "Summary trial", "phase": "II"}, headers=headers)

    summary = client.get("/api/clinical/summary", headers=headers)
    assert summary.status_code == 200
    assert summary.json()["total_trials"] >= 1


def test_creating_trial_requires_elevated_role(client, db_session):
    headers = auth_headers(client, db_session, "plain-user@larkai.test")
    resp = client.post(
        "/api/clinical/trials", json={"title": "Should be denied", "phase": "I"}, headers=headers
    )
    assert resp.status_code == 403
