def _auth_headers(client, email="ops-lead@larkai.test"):
    client.post("/api/auth/register", json={"email": email, "password": "supersecret123", "full_name": "Ops Lead"})
    login = client.post("/api/auth/login", json={"email": email, "password": "supersecret123"})
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def _sample_steps():
    return [
        {
            "name": "Notify ops",
            "type": "send_notification",
            "config": {"user_id": "placeholder", "title": "Workflow ran"},
        }
    ]


def test_create_list_and_get_workflow(client):
    headers = _auth_headers(client)

    create_resp = client.post(
        "/api/workflows",
        json={"name": "Weekly ops check", "description": "Nudges the ops channel", "steps": _sample_steps()},
        headers=headers,
    )
    assert create_resp.status_code == 201
    workflow = create_resp.json()
    assert workflow["name"] == "Weekly ops check"
    assert workflow["trigger_type"] == "manual"
    assert workflow["is_active"] is True
    assert len(workflow["steps"]) == 1

    listing = client.get("/api/workflows", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["total"] >= 1

    get_resp = client.get(f"/api/workflows/{workflow['id']}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == workflow["id"]


def test_update_workflow_steps(client):
    headers = _auth_headers(client, "ops2@larkai.test")
    workflow = client.post(
        "/api/workflows", json={"name": "Renamed later", "steps": []}, headers=headers
    ).json()

    patch_resp = client.patch(
        f"/api/workflows/{workflow['id']}",
        json={"name": "Actually renamed", "steps": _sample_steps()},
        headers=headers,
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["name"] == "Actually renamed"
    assert len(patch_resp.json()["steps"]) == 1


def test_cannot_trigger_workflow_with_no_steps(client):
    headers = _auth_headers(client, "ops3@larkai.test")
    workflow = client.post("/api/workflows", json={"name": "Empty workflow", "steps": []}, headers=headers).json()

    run_resp = client.post(f"/api/workflows/{workflow['id']}/run", headers=headers)
    assert run_resp.status_code == 400
    assert run_resp.json()["error"] == "workflow_empty"


def test_cannot_trigger_inactive_workflow(client):
    headers = _auth_headers(client, "ops4@larkai.test")
    workflow = client.post(
        "/api/workflows", json={"name": "Disabled", "steps": _sample_steps()}, headers=headers
    ).json()
    client.patch(f"/api/workflows/{workflow['id']}", json={"is_active": False}, headers=headers)

    run_resp = client.post(f"/api/workflows/{workflow['id']}/run", headers=headers)
    assert run_resp.status_code == 400
    assert run_resp.json()["error"] == "workflow_inactive"


def test_trigger_run_creates_pending_run_and_is_listed(client):
    """Verifies the API-visible half of triggering a run: a WorkflowRun row
    is created and returned as "pending". Actually executing its steps
    happens in a separate Celery worker process (app/tasks/workflows.py),
    which needs a live broker — outside what these in-process API tests
    exercise, same as the report-generation Celery task."""
    headers = _auth_headers(client, "ops5@larkai.test")
    workflow = client.post(
        "/api/workflows", json={"name": "Trigger me", "steps": _sample_steps()}, headers=headers
    ).json()

    run_resp = client.post(f"/api/workflows/{workflow['id']}/run", headers=headers)
    assert run_resp.status_code == 202
    run = run_resp.json()
    assert run["workflow_id"] == workflow["id"]
    assert run["status"] in ("pending", "running", "succeeded", "failed")

    runs_listing = client.get(f"/api/workflows/{workflow['id']}/runs", headers=headers)
    assert runs_listing.status_code == 200
    assert runs_listing.json()["total"] >= 1

    run_detail = client.get(f"/api/workflows/runs/{run['id']}", headers=headers)
    assert run_detail.status_code == 200
    assert run_detail.json()["id"] == run["id"]
    assert "step_runs" in run_detail.json()


def test_get_unknown_workflow_returns_404(client):
    headers = _auth_headers(client, "ops6@larkai.test")
    resp = client.get("/api/workflows/does-not-exist", headers=headers)
    assert resp.status_code == 404
