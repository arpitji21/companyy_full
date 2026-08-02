from tests.conftest import auth_headers


def test_create_and_list_orders(client, db_session):
    headers = auth_headers(client, db_session, "procurement-lead@larkai.test", role_name="Manager")

    create_resp = client.post(
        "/api/procurement/orders",
        json={"title": "Lab reagents restock", "category": "supplies", "amount": "2500.00"},
        headers=headers,
    )
    assert create_resp.status_code == 201
    order = create_resp.json()
    assert order["title"] == "Lab reagents restock"
    assert order["status"] == "requested"

    listing = client.get("/api/procurement/orders?category=supplies", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["total"] >= 1

    get_resp = client.get(f"/api/procurement/orders/{order['id']}", headers=headers)
    assert get_resp.status_code == 200


def test_update_order_status(client, db_session):
    headers = auth_headers(client, db_session, "procurement-lead2@larkai.test", role_name="Manager")
    order = client.post("/api/procurement/orders", json={"title": "New laptops"}, headers=headers).json()

    update_resp = client.patch(
        f"/api/procurement/orders/{order['id']}", json={"status": "ordered"}, headers=headers
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "ordered"


def test_summary_totals_spend(client, db_session):
    headers = auth_headers(client, db_session, "procurement-lead3@larkai.test", role_name="Manager")
    client.post(
        "/api/procurement/orders",
        json={"title": "Office supplies", "category": "office", "amount": "300.00"},
        headers=headers,
    )

    summary = client.get("/api/procurement/summary", headers=headers)
    assert summary.status_code == 200
    assert summary.json()["total_orders"] >= 1


def test_creating_order_requires_elevated_role(client, db_session):
    headers = auth_headers(client, db_session, "plain-user@larkai.test")
    resp = client.post("/api/procurement/orders", json={"title": "Should be denied"}, headers=headers)
    assert resp.status_code == 403
