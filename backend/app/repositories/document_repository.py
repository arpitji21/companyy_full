from sqlalchemy import func, select

from app.models.document import Document
from app.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    model = Document

    def counts_by_folder(self) -> dict[str, int]:
        rows = self.db.execute(
            select(Document.folder, func.count()).group_by(Document.folder)
        ).all()
        return {(folder or "Uncategorized"): count for folder, count in rows}

    def total_size_bytes(self) -> int:
        return self.db.scalar(select(func.coalesce(func.sum(Document.size_bytes), 0))) or 0
