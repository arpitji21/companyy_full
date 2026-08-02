def _auth_headers(client, email):
    client.post("/api/auth/register", json={"email": email, "password": "supersecret123", "full_name": "Tester"})
    login = client.post("/api/auth/login", json={"email": email, "password": "supersecret123"})
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_sales_pipeline_summary(client):
    headers = _auth_headers(client, "sales@larkai.test")

    customer_resp = client.post("/api/sales/customers", json={"name": "Acme Corp"}, headers=headers)
    assert customer_resp.status_code == 201
    customer_id = customer_resp.json()["id"]

    deal_resp = client.post(
        "/api/sales/deals",
        json={"customer_id": customer_id, "deal_name": "Acme Renewal", "amount": "50000.00", "probability": 60},
        headers=headers,
    )
    assert deal_resp.status_code == 201

    summary = client.get("/api/sales/summary", headers=headers)
    assert summary.status_code == 200
    assert float(summary.json()["total_pipeline_value"]) == 50000.0


def test_marketing_campaign_summary(client):
    headers = _auth_headers(client, "cmo@larkai.test")

    client.post(
        "/api/marketing/campaigns",
        json={"name": "Summer Push", "channel": "social", "status": "live"},
        headers=headers,
    )
    resp = client.get("/api/marketing/summary", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["total_campaigns"] == 1
    assert resp.json()["active_campaigns"] == 1


def test_manufacturing_and_quality(client):
    headers = _auth_headers(client, "ops@larkai.test")

    batch_resp = client.post(
        "/api/manufacturing/batches",
        json={"batch_number": "B-1001", "product_name": "Widget X", "quantity_produced": 500},
        headers=headers,
    )
    assert batch_resp.status_code == 201
    batch_id = batch_resp.json()["id"]

    check_resp = client.post(
        "/api/quality/checks",
        json={"batch_id": batch_id, "check_type": "inspection", "result": "pass"},
        headers=headers,
    )
    assert check_resp.status_code == 201

    metrics = client.get("/api/quality/metrics", headers=headers)
    assert metrics.status_code == 200
    assert metrics.json()["pass_count"] == 1


def test_compliance_and_regulatory(client):
    headers = _auth_headers(client, "compliance@larkai.test")

    resp = client.post(
        "/api/compliance/records",
        json={"framework": "ISO", "title": "ISO 9001 Cert", "status": "approved"},
        headers=headers,
    )
    assert resp.status_code == 201

    summary = client.get("/api/compliance/summary", headers=headers)
    assert summary.status_code == 200
    assert summary.json()["approved"] == 1

    reg_list = client.get("/api/regulatory/submissions", headers=headers)
    assert reg_list.status_code == 200
    assert reg_list.json()["total"] == 1


def test_supply_chain(client):
    headers = _auth_headers(client, "procurement@larkai.test")

    vendor_resp = client.post("/api/supply-chain/vendors", json={"name": "Global Supplies Inc"}, headers=headers)
    assert vendor_resp.status_code == 201

    item_resp = client.post(
        "/api/supply-chain/inventory",
        json={"sku": "SKU-001", "name": "Steel Bolts", "quantity_on_hand": 5, "reorder_level": 20},
        headers=headers,
    )
    assert item_resp.status_code == 201

    summary = client.get("/api/supply-chain/summary", headers=headers)
    assert summary.status_code == 200
    assert summary.json()["items_below_reorder_level"] == 1
