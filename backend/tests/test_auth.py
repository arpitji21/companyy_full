def test_register_and_login(client):
    register_resp = client.post(
        "/api/auth/register",
        json={"email": "ceo@larkai.test", "password": "supersecret123", "full_name": "Ada CEO"},
    )
    assert register_resp.status_code == 201
    body = register_resp.json()
    assert body["email"] == "ceo@larkai.test"
    assert "hashed_password" not in body  # never leak the hash

    login_resp = client.post(
        "/api/auth/login",
        json={"email": "ceo@larkai.test", "password": "supersecret123"},
    )
    assert login_resp.status_code == 200
    tokens = login_resp.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    me_resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "ceo@larkai.test"


def test_login_wrong_password(client):
    client.post(
        "/api/auth/register",
        json={"email": "user@larkai.test", "password": "correcthorsebattery", "full_name": "Regular User"},
    )
    resp = client.post(
        "/api/auth/login",
        json={"email": "user@larkai.test", "password": "wrong-password"},
    )
    assert resp.status_code == 401


def test_me_requires_auth(client):
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_health_check(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
