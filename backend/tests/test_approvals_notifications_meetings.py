from app.models.department import Department
from tests.conftest import auth_headers


# ---------------------------------------------------------------------------
# Approvals — the decision flow itself (test_phase3.py only covers create +
# list), and that approving/rejecting resolves the notification it raised.
# ---------------------------------------------------------------------------


def test_approving_a_request_notifies_and_then_resolves_the_notification(client, db_session):
    # This user holds the CEO role, so ApprovalService.create's notify_role
    # fan-out (see app/services/approval_service.py) reaches them directly —
    # letting this test check the notification lifecycle end-to-end.
    headers = auth_headers(client, db_session, "ceo-approver@larkai.test", role_name="CEO")

    approval = client.post(
        "/api/approvals", json={"title": "New vendor contract", "amount": "5000.00"}, headers=headers
    ).json()

    unread_before = client.get("/api/notifications/unread-count", headers=headers).json()
    assert unread_before["unread_count"] >= 1

    decision = client.post(
        f"/api/approvals/{approval['id']}/decision",
        json={"approve": True, "notes": "Looks good"},
        headers=headers,
    )
    assert decision.status_code == 200
    assert decision.json()["status"] == "approved"
    assert decision.json()["notes"] == "Looks good"

    unread_after = client.get("/api/notifications/unread-count", headers=headers).json()
    assert unread_after["unread_count"] == unread_before["unread_count"] - 1


def test_rejecting_a_request_sets_rejected_status(client, db_session):
    headers = auth_headers(client, db_session, "ceo-approver2@larkai.test", role_name="CEO")
    approval = client.post("/api/approvals", json={"title": "Risky spend"}, headers=headers).json()

    decision = client.post(
        f"/api/approvals/{approval['id']}/decision",
        json={"approve": False, "notes": "Not now"},
        headers=headers,
    )
    assert decision.status_code == 200
    assert decision.json()["status"] == "rejected"


def test_deciding_an_approval_requires_elevated_role(client, db_session):
    headers = auth_headers(client, db_session, "plain-user@larkai.test")
    approval = client.post("/api/approvals", json={"title": "Anything"}, headers=headers).json()

    resp = client.post(f"/api/approvals/{approval['id']}/decision", json={"approve": True}, headers=headers)
    assert resp.status_code == 403


def test_deciding_an_unknown_approval_returns_404(client, db_session):
    headers = auth_headers(client, db_session, "ceo-approver3@larkai.test", role_name="CEO")
    resp = client.post("/api/approvals/does-not-exist/decision", json={"approve": True}, headers=headers)
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Notifications — creation (admin-only), marking read, the unread_only
# filter, and ownership enforcement.
# ---------------------------------------------------------------------------


def test_admin_can_create_notification_for_a_user(client, db_session):
    headers = auth_headers(client, db_session, "admin-notif@larkai.test", role_name="Admin")
    # NotificationCreate needs a real user_id — use the admin's own account.
    me = client.get("/api/auth/me", headers=headers).json()

    create_resp = client.post(
        "/api/notifications",
        json={"user_id": me["id"], "type": "system", "title": "Scheduled maintenance tonight"},
        headers=headers,
    )
    assert create_resp.status_code == 201
    assert create_resp.json()["is_read"] is False


def test_creating_notification_requires_elevated_role(client, db_session):
    headers = auth_headers(client, db_session, "plain-user2@larkai.test")
    me = client.get("/api/auth/me", headers=headers).json()

    resp = client.post(
        "/api/notifications",
        json={"user_id": me["id"], "type": "system", "title": "Should be denied"},
        headers=headers,
    )
    assert resp.status_code == 403


def test_mark_read_and_unread_only_filter(client, db_session):
    headers = auth_headers(client, db_session, "admin-notif2@larkai.test", role_name="Admin")
    me = client.get("/api/auth/me", headers=headers).json()

    notification = client.post(
        "/api/notifications",
        json={"user_id": me["id"], "type": "system", "title": "Check this out"},
        headers=headers,
    ).json()

    unread_listing = client.get("/api/notifications?unread_only=true", headers=headers)
    assert any(n["id"] == notification["id"] for n in unread_listing.json()["items"])

    mark_resp = client.post(f"/api/notifications/{notification['id']}/read", headers=headers)
    assert mark_resp.status_code == 200
    assert mark_resp.json()["is_read"] is True

    unread_listing_after = client.get("/api/notifications?unread_only=true", headers=headers)
    assert all(n["id"] != notification["id"] for n in unread_listing_after.json()["items"])


def test_cannot_mark_another_users_notification_as_read(client, db_session):
    admin_headers = auth_headers(client, db_session, "admin-notif3@larkai.test", role_name="Admin")
    other_headers = auth_headers(client, db_session, "other-user@larkai.test")
    other_me = client.get("/api/auth/me", headers=other_headers).json()

    notification = client.post(
        "/api/notifications",
        json={"user_id": other_me["id"], "type": "system", "title": "For someone else"},
        headers=admin_headers,
    ).json()

    # admin (not the notification's owner) tries to mark it read
    resp = client.post(f"/api/notifications/{notification['id']}/read", headers=admin_headers)
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Meetings — the department_id filter (test_phase3.py only covers create +
# upcoming with no filter).
# ---------------------------------------------------------------------------


def test_meetings_filter_by_department(client, db_session):
    headers = auth_headers(client, db_session, "meetings-user@larkai.test")

    dept = Department(name="Finance Test Dept", slug="finance-test-dept")
    db_session.add(dept)
    db_session.commit()
    db_session.refresh(dept)

    client.post(
        "/api/meetings",
        json={"title": "Finance sync", "department_id": dept.id, "starts_at": "2026-08-05T09:00:00Z"},
        headers=headers,
    )
    client.post(
        "/api/meetings",
        json={"title": "No department meeting", "starts_at": "2026-08-06T09:00:00Z"},
        headers=headers,
    )

    filtered = client.get(f"/api/meetings?department_id={dept.id}", headers=headers)
    assert filtered.status_code == 200
    items = filtered.json()["items"]
    assert len(items) >= 1
    assert all(m["department_id"] == dept.id for m in items)
