from pydantic import BaseModel, ConfigDict


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    folder: str | None
    department_id: str | None
    uploaded_by: str | None
    s3_key: str
    mime_type: str | None
    size_bytes: int | None
    version: int
    ai_summary: str | None


class DocumentUpdate(BaseModel):
    name: str | None = None
    folder: str | None = None
    version: int | None = None
    ai_summary: str | None = None


class DocumentSummary(BaseModel):
    total_documents: int
    total_size_bytes: int
    by_folder: dict[str, int]
