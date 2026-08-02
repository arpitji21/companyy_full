import pytest
from fastapi import WebSocketDisconnect

from app.websocket.manager import ConnectionManager
from tests.conftest import auth_headers

WS_PATH = "/api/ws/notifications"


# ---------------------------------------------------------------------------
# Route-level: the actual /api/ws/notifications endpoint, via TestClient's
# websocket_connect. Exercises real auth + the heartbeat protocol; doesn't
# touch Redis (that's the listener/publisher side, covered separately below
# at the unit level — pushing a message through real Redis pub/sub isn't
# something an in-process test can exercise without a live Redis).
# ---------------------------------------------------------------------------


def test_ws_rejects_connection_with_no_token(client):
    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect(WS_PATH):
            pass
    assert exc_info.value.code == 4401


def test_ws_rejects_connection_with_garbage_token(client):
    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect(f"{WS_PATH}?token=not-a-real-jwt"):
            pass
    assert exc_info.value.code == 4401


def test_ws_accepts_valid_token_and_answers_heartbeat(client, db_session):
    headers = auth_headers(client, db_session, "ws-user@larkai.test")
    token = headers["Authorization"].split(" ", 1)[1]

    with client.websocket_connect(f"{WS_PATH}?token={token}") as ws:
        ws.send_text("ping")
        assert ws.receive_text() == "pong"


def test_ws_rejects_expired_or_wrong_type_token(client, db_session):
    """A refresh token (type != "access") must be rejected the same way an
    invalid one is — the socket only accepts short-lived access tokens."""
    headers = auth_headers(client, db_session, "ws-user2@larkai.test")
    access_token = headers["Authorization"].split(" ", 1)[1]

    login_resp = client.post(
        "/api/auth/login", json={"email": "ws-user2@larkai.test", "password": "supersecret123"}
    )
    refresh_token = login_resp.json()["refresh_token"]
    assert refresh_token != access_token  # sanity check we're actually using the other token

    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect(f"{WS_PATH}?token={refresh_token}"):
            pass
    assert exc_info.value.code == 4401


# ---------------------------------------------------------------------------
# Unit-level: ConnectionManager's fan-out logic, independent of the WS route
# or Redis. Fast and deterministic — no event loop juggling with TestClient's
# background thread.
# ---------------------------------------------------------------------------


class _FakeWebSocket:
    """Minimal stand-in for FastAPI's WebSocket — just enough surface for
    ConnectionManager to call send_json on."""

    def __init__(self, *, fail: bool = False):
        self.fail = fail
        self.sent: list[dict] = []

    async def send_json(self, payload: dict) -> None:
        if self.fail:
            raise RuntimeError("connection closed")
        self.sent.append(payload)


@pytest.mark.asyncio
async def test_manager_delivers_to_connected_user():
    manager = ConnectionManager()
    ws = _FakeWebSocket()
    await manager.connect("user-1", ws)

    delivered = await manager.send_to_user("user-1", {"title": "New approval request"})

    assert delivered == 1
    assert ws.sent == [{"title": "New approval request"}]


@pytest.mark.asyncio
async def test_manager_returns_zero_for_a_user_with_no_local_connection():
    manager = ConnectionManager()
    delivered = await manager.send_to_user("nobody-connected", {"title": "..."})
    assert delivered == 0


@pytest.mark.asyncio
async def test_manager_fans_out_to_multiple_sockets_for_the_same_user():
    """A user open in two browser tabs should get the push in both."""
    manager = ConnectionManager()
    tab1, tab2 = _FakeWebSocket(), _FakeWebSocket()
    await manager.connect("user-1", tab1)
    await manager.connect("user-1", tab2)

    delivered = await manager.send_to_user("user-1", {"title": "Broadcast"})

    assert delivered == 2
    assert tab1.sent == [{"title": "Broadcast"}]
    assert tab2.sent == [{"title": "Broadcast"}]


@pytest.mark.asyncio
async def test_manager_drops_dead_socket_on_send_failure():
    manager = ConnectionManager()
    dead_ws = _FakeWebSocket(fail=True)
    await manager.connect("user-1", dead_ws)

    delivered = await manager.send_to_user("user-1", {"title": "..."})

    assert delivered == 0
    assert manager.local_connection_count() == 0  # the dead socket was cleaned up, not left dangling


@pytest.mark.asyncio
async def test_manager_disconnect_removes_only_that_socket():
    manager = ConnectionManager()
    tab1, tab2 = _FakeWebSocket(), _FakeWebSocket()
    await manager.connect("user-1", tab1)
    await manager.connect("user-1", tab2)

    await manager.disconnect("user-1", tab1)

    assert manager.local_connection_count() == 1
    delivered = await manager.send_to_user("user-1", {"title": "Still here"})
    assert delivered == 1
    assert tab2.sent == [{"title": "Still here"}]
