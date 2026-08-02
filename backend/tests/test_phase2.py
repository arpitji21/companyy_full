def _auth_headers(client, email="admin@larkai.test"):
    client.post("/api/auth/register", json={"email": email, "password": "supersecret123", "full_name": "Admin"})
    login = client.post("/api/auth/login", json={"email": email, "password": "supersecret123"})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_department_and_employee_flow(client):
    headers = _auth_headers(client)

    dept_resp = client.post(
        "/api/departments", json={"name": "Finance", "slug": "finance", "icon": "💰"}, headers=headers
    )
    assert dept_resp.status_code == 201
    dept_id = dept_resp.json()["id"]

    emp_resp = client.post(
        "/api/employees",
        json={"full_name": "Jamie Lee", "email": "jamie@larkai.test", "department_id": dept_id, "job_title": "Analyst"},
        headers=headers,
    )
    assert emp_resp.status_code == 201
    assert emp_resp.json()["department_id"] == dept_id

    list_resp = client.get("/api/employees", headers=headers)
    assert list_resp.status_code == 200
    assert list_resp.json()["total"] >= 1

    headcount = client.get("/api/hr/headcount", headers=headers)
    assert headcount.status_code == 200
    assert headcount.json()["total_employees"] >= 1


def test_project_and_task_flow(client):
    headers = _auth_headers(client, email="pm@larkai.test")

    project_resp = client.post("/api/projects", json={"name": "Q3 Launch"}, headers=headers)
    assert project_resp.status_code == 201
    project_id = project_resp.json()["id"]

    task_resp = client.post(
        f"/api/projects/{project_id}/tasks", json={"title": "Draft launch plan"}, headers=headers
    )
    assert task_resp.status_code == 201
    task_id = task_resp.json()["id"]

    update_resp = client.patch(f"/api/projects/tasks/{task_id}", json={"status": "in_progress"}, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "in_progress"


def test_finance_transactions_and_summary(client):
    headers = _auth_headers(client, email="cfo@larkai.test")

    client.post(
        "/api/finance/transactions",
        json={"type": "revenue", "amount": "10000.00", "transaction_date": "2026-07-01"},
        headers=headers,
    )
    client.post(
        "/api/finance/transactions",
        json={"type": "expense", "category": "payroll", "amount": "4000.00", "transaction_date": "2026-07-05"},
        headers=headers,
    )

    summary_resp = client.get("/api/finance/summary", headers=headers)
    assert summary_resp.status_code == 200
    body = summary_resp.json()
    assert float(body["total_revenue"]) == 10000.0
    assert float(body["total_expenses"]) == 4000.0
    assert float(body["net_cash_flow"]) == 6000.0
