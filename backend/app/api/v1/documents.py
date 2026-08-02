from urllib.parse import quote

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.db.session import get_db
from app.schemas.common import Page
from app.schemas.document import DocumentRead, DocumentSummary, DocumentUpdate
from app.services.document_service import DocumentService
from app.utils.pagination import PaginationParams, build_page

router = APIRouter(prefix="/documents", tags=["Documents"])

# Real object-storage-backed file upload/download, on top of the
# `documents` table (name, folder, s3_key, mime_type, size_bytes, version).
# See app/storage/__init__.py for the S3 client and app/services/
# file_scanning.py for the size/type/virus checks every upload goes
# through before it reaches the bucket.


@router.get("/summary", response_model=DocumentSummary)
def get_summary(db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return DocumentService(db).summary()


@router.get("", response_model=Page[DocumentRead])
def list_documents(
    folder: str | None = None,
    department_id: str | None = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    items, total = DocumentService(db).list(
        pagination.page, pagination.page_size, folder=folder, department_id=department_id
    )
    return build_page(items, total, pagination.page, pagination.page_size)


@router.post("/upload", response_model=DocumentRead, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    name: str | None = Form(None),
    folder: str | None = Form(None),
    department_id: str | None = Form(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user),
):
    # Read the whole upload before handing off to the service: size/type/
    # virus checks all need the complete bytes anyway, and FastAPI's
    # UploadFile already spools large uploads to a temp file under the
    # hood, so this doesn't blow up memory for reasonably-sized documents.
    data = await file.read()

    return DocumentService(db).upload(
        data=data,
        filename=file.filename or "upload",
        display_name=name,
        folder=folder,
        department_id=department_id,
        uploaded_by=user.id,
    )


@router.get("/{document_id}", response_model=DocumentRead)
def get_document(document_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    return DocumentService(db).get(document_id)


@router.get("/{document_id}/download")
def download_document(document_id: str, db: Session = Depends(get_db), _=Depends(get_current_active_user)):
    body_stream, mime_type, filename, content_length = DocumentService(db).download(document_id)

    headers = {
        # Both forms so older clients that don't understand filename* still
        # get a sane (ASCII-safe) name, while modern ones get the exact one.
        "Content-Disposition": (
            f'attachment; filename="{quote(filename, safe="")}"; '
            f"filename*=UTF-8''{quote(filename, safe='')}"
        ),
    }
    if content_length is not None:
        headers["Content-Length"] = str(content_length)

    return StreamingResponse(
        body_stream.iter_chunks(),
        media_type=mime_type or "application/octet-stream",
        headers=headers,
    )


@router.patch("/{document_id}", response_model=DocumentRead)
def update_document(
    document_id: str,
    payload: DocumentUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles("CEO", "Admin")),
):
    return DocumentService(db).update(document_id, payload)
