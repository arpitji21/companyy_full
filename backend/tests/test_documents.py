from tests.conftest import auth_headers


def test_upload_list_get_and_update_document(client, db_session, monkeypatch):
    """S3 isn't configured in tests (no S3_ACCESS_KEY/S3_SECRET_KEY), and
    app.storage.upload_bytes no-ops in that case — see app/storage/__init__.py.
    Monkeypatching it here simulates a configured bucket so the upload path
    can be exercised end-to-end without real AWS credentials."""
    monkeypatch.setattr(
        "app.services.document_service.storage.upload_bytes",
        lambda key, data, content_type=None: key,
    )

    headers = auth_headers(client, db_session, "docs-lead@larkai.test")

    upload_resp = client.post(
        "/api/documents/upload",
        files={"file": ("policy.txt", b"Standard operating procedure text.", "text/plain")},
        data={"folder": "Policies"},
        headers=headers,
    )
    assert upload_resp.status_code == 201
    document = upload_resp.json()
    assert document["name"] == "policy.txt"
    assert document["folder"] == "Policies"

    listing = client.get("/api/documents?folder=Policies", headers=headers)
    assert listing.status_code == 200
    assert listing.json()["total"] >= 1

    get_resp = client.get(f"/api/documents/{document['id']}", headers=headers)
    assert get_resp.status_code == 200

    summary = client.get("/api/documents/summary", headers=headers)
    assert summary.status_code == 200
    assert summary.json()["total_documents"] >= 1


def test_upload_without_storage_configured_returns_503(client, db_session):
    """Without the monkeypatch above, S3 is genuinely unconfigured in
    tests — uploads should fail clearly (503), not silently succeed with
    no file actually stored anywhere."""
    headers = auth_headers(client, db_session, "docs-lead2@larkai.test")

    resp = client.post(
        "/api/documents/upload",
        files={"file": ("notes.txt", b"some notes", "text/plain")},
        headers=headers,
    )
    assert resp.status_code == 503


def test_dangerous_file_extension_is_rejected(client, db_session, monkeypatch):
    monkeypatch.setattr(
        "app.services.document_service.storage.upload_bytes",
        lambda key, data, content_type=None: key,
    )
    headers = auth_headers(client, db_session, "docs-lead3@larkai.test")

    resp = client.post(
        "/api/documents/upload",
        files={"file": ("payload.exe", b"MZ...", "application/octet-stream")},
        headers=headers,
    )
    assert resp.status_code == 415


def test_updating_document_requires_elevated_role(client, db_session, monkeypatch):
    monkeypatch.setattr(
        "app.services.document_service.storage.upload_bytes",
        lambda key, data, content_type=None: key,
    )
    headers = auth_headers(client, db_session, "docs-lead4@larkai.test")
    upload_resp = client.post(
        "/api/documents/upload",
        files={"file": ("report.txt", b"content", "text/plain")},
        headers=headers,
    )
    document = upload_resp.json()

    resp = client.patch(f"/api/documents/{document['id']}", json={"name": "renamed.txt"}, headers=headers)
    assert resp.status_code == 403
