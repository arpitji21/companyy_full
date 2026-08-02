from app.models.manufacturing import QualityCheck
from app.repositories.manufacturing_repository import QualityCheckRepository
from app.schemas.manufacturing import QualityCheckCreate, QualityMetrics


class QualityService:
    def __init__(self, db):
        self.db = db
        self.repo = QualityCheckRepository(db)

    def list(self, page: int, page_size: int, check_type: str | None = None, result: str | None = None):
        return self.repo.list(page=page, page_size=page_size, check_type=check_type, result=result)

    def create(self, data: QualityCheckCreate) -> QualityCheck:
        return self.repo.create(QualityCheck(**data.model_dump()))

    def metrics(self) -> QualityMetrics:
        by_result = self.repo.counts_by_result()
        total = sum(by_result.values())
        passed = by_result.get("pass", 0)
        pass_rate = (passed / total * 100) if total else 0.0
        return QualityMetrics(
            total_checks=total,
            pass_count=passed,
            fail_count=by_result.get("fail", 0),
            pending_count=by_result.get("pending", 0),
            pass_rate=round(pass_rate, 2),
        )
