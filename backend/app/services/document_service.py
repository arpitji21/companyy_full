import re
import uuid

from app import storage
from app.core.exceptions import NotFoundError, StorageNotConfiguredError
from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentSummary, DocumentUpdate
from app.services import file_scanning

_SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


def _safe_filename(filename: str) -> str:
    """Strips path components and anything that isn't a safe filename
    character, so the original filename can't be used to escape the
    intended S3 prefix (e.g. "../../etc/passwd") or inject odd bytes into
    the object key."""
    name = filename.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    name = _SAFE_NAME_RE.sub("_", name).strip("._") or "file"
    return name[:200]


class DocumentService:
    def __init__(self, db):
        self.db = db
        self.repo = DocumentRepository(db)

    def list(self, page: int, page_size: int, folder: str | None = None, department_id: str | None = None):
        return self.repo.list(page=page, page_size=page_size, folder=folder, department_id=department_id)

    def get(self, document_id: str) -> Document:
        document = self.repo.get(document_id)
        if not document:
            raise NotFoundError("Document not found.")
        return document

    def upload(
        self,
        *,
        data: bytes,
        filename: str,
        display_name: str | None,
        folder: str | None,
        department_id: str | None,
        uploaded_by: str | None,
    ) -> Document:
        """Validates, scans, and uploads a file's bytes to object storage,
        then records the resulting Document row. This is the only path
        that creates a document with real, verified content behind it —
        see file_scanning.py for what "validates and scans" means."""
        file_scanning.validate_file_size(len(data))
        sniffed_mime_type = file_scanning.validate_file_type(filename, data)
        file_scanning.scan_for_virus(data)

        safe_name = _safe_filename(filename)
        s3_key = f"documents/{uuid.uuid4()}/{safe_name}"

        stored_key = storage.upload_bytes(s3_key, data, content_type=sniffed_mime_type)
        if not stored_key:
            raise StorageNotConfiguredError(
                "Object storage isn't configured yet. Set S3_ACCESS_KEY/S3_SECRET_KEY "
                "(and S3_ENDPOINT_URL for a non-AWS S3-compatible provider) to enable uploads."
            )

        document = Document(
            name=display_name or filename,
            folder=folder,
            department_id=department_id,
            uploaded_by=uploaded_by,
            s3_key=stored_key,
            mime_type=sniffed_mime_type,
            size_bytes=len(data),
            version=1,
        )
        return self.repo.create(document)

    def download(self, document_id: str):
        """Returns (body_stream, mime_type, filename, content_length) for
        streaming a document's bytes back to the client. `mime_type` is the
        type recorded at upload time (trusted, since it was verified by
        file_scanning at upload) rather than anything S3 reports."""
        document = self.get(document_id)

        result = storage.get_object_stream(document.s3_key)
        if result is None:
            raise StorageNotConfiguredError(
                "Object storage isn't configured, or this document's file is no longer "
                "in the bucket. Its metadata still exists, but the content can't be fetched."
            )
        body_stream, s3_content_type, content_length = result
        mime_type = document.mime_type or s3_content_type
        return body_stream, mime_type, document.name, content_length

    def update(self, document_id: str, data: DocumentUpdate) -> Document:
        document = self.get(document_id)
        payload = data.model_dump(exclude_unset=True)
        # A rename or content change bumps the version instead of silently
        # overwriting it, so /documents keeps a lightweight history signal
        # even before a real version-diff store exists.
        if payload and "version" not in payload:
            payload["version"] = document.version + 1
        return self.repo.update(document, payload)

    def summary(self) -> DocumentSummary:
        by_folder = self.repo.counts_by_folder()
        return DocumentSummary(
            total_documents=sum(by_folder.values()),
            total_size_bytes=self.repo.total_size_bytes(),
            by_folder=by_folder,
        )
