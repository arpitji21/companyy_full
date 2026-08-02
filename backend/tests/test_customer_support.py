from tests.conftest import auth_headers


def test_create_and_list_tickets(client, db_session):
    headers = auth_headers(client, db_session, "support-lead@larkai.test", role_name="Manager")

    create_resp = client.post(
        "/api/customer/tickets",
        json={"subject": "Login broken", "priority": "high"},
        headers=headers,
    )
    assert create_resp.status_code == 201
    ticket = create_resp.json()
    assert ticket["subject"] == "Login broken"
    assert ticket["status"] == "open"

    listing = client.get("/api/customer/tickets?status=open", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["total"] >= 1

    get_resp = client.get(f"/api/customer/tickets/{ticket['id']}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == ticket["id"]


def test_update_ticket_status(client, db_session):
    headers = auth_headers(client, db_session, "support-lead2@larkai.test", role_name="Manager")
    ticket = client.post("/api/customer/tickets", json={"subject": "Billing question"}, headers=headers).json()

    update_resp = client.patch(
        f"/api/customer/tickets/{ticket['id']}",
        json={"status": "resolved", "csat_score": "4.5"},
        headers=headers,
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "resolved"


def test_summary_reflects_tickets(client, db_session):
    headers = auth_headers(client, db_session, "support-lead3@larkai.test", role_name="Manager")
    client.post("/api/customer/tickets", json={"subject": "Onboarding help"}, headers=headers)

    summary = client.get("/api/customer/summary", headers=headers)
    assert summary.status_code == 200
    assert summary.json()["total_tickets"] >= 1


def test_creating_ticket_requires_elevated_role(client, db_session):
    headers = auth_headers(client, db_session, "plain-user@larkai.test")
    resp = client.post("/api/customer/tickets", json={"subject": "Should be denied"}, headers=headers)
    assert resp.status_code == 403
