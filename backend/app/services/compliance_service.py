from app.core.exceptions import NotFoundError
from app.models.compliance import ComplianceRecord
from app.repositories.compliance_repository import ComplianceRepository
from app.schemas.compliance import ComplianceRecordCreate, ComplianceRecordUpdate, ComplianceSummary


class ComplianceService:
    def __init__(self, db):
        self.db = db
        self.repo = ComplianceRepository(db)

    def list(self, page: int, page_size: int, framework: str | None = None, status: str | None = None):
        return self.repo.list(page=page, page_size=page_size, framework=framework, status=status)

    def create(self, data: ComplianceRecordCreate) -> ComplianceRecord:
        return self.repo.create(ComplianceRecord(**data.model_dump()))

    def update(self, record_id: str, data: ComplianceRecordUpdate) -> ComplianceRecord:
        record = self.repo.get(record_id)
        if not record:
            raise NotFoundError("Compliance record not found.")
        return self.repo.update(record, data.model_dump(exclude_unset=True))

    def summary(self) -> ComplianceSummary:
        by_status = self.repo.counts_by_status()
        total = sum(by_status.values())
        approved = by_status.get("approved", 0)
        score = (approved / total * 100) if total else 100.0
        return ComplianceSummary(
            total_records=total,
            approved=approved,
            expired=by_status.get("expired", 0),
            in_progress=by_status.get("in_progress", 0),
            compliance_score=round(score, 2),
        )
