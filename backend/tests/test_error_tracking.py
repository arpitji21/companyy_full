from app.core.error_tracking import setup_sentry


def test_setup_sentry_is_noop_without_dsn(monkeypatch):
    """With no SENTRY_DSN configured (the default in dev/test/CI), calling
    setup_sentry() must do nothing and must not raise — Sentry stays fully
    optional."""
    monkeypatch.setattr("app.core.error_tracking.settings.SENTRY_DSN", None)
    setup_sentry()  # should not raise


def test_app_boots_with_sentry_setup_wired_in(client):
    """create_app() calls setup_sentry() during startup; the app fixture
    booting successfully (via TestClient) confirms that call doesn't break
    app startup when SENTRY_DSN is unset."""
    response = client.get("/docs")
    assert response.status_code == 200
