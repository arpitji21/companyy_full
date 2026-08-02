import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.models.user import Role
from main import app

# SQLite in-memory for fast, isolated test runs. Production uses Postgres —
# this is fine for exercising API/service logic, not for testing Postgres-
# specific SQL.
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def auth_headers(client, db_session, email, *, role_name: str | None = None):
    """Registers (and logs in) a user, returning Authorization headers.

    If role_name is given, the role is inserted directly via db_session
    first (a fresh test DB has no seeded roles — the seed script that
    creates them in a real deployment doesn't run here), then passed to
    /auth/register so the new user is created already holding it. This is
    what lets tests exercise `require_roles(...)`-gated endpoints for real,
    rather than only checking the 403 a plain user gets.
    """
    if role_name and not db_session.query(Role).filter_by(name=role_name).first():
        db_session.add(Role(name=role_name))
        db_session.commit()

    payload = {"email": email, "password": "supersecret123", "full_name": "Test User"}
    if role_name:
        payload["role_name"] = role_name
    client.post("/api/auth/register", json=payload)

    login = client.post("/api/auth/login", json={"email": email, "password": "supersecret123"})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
