from app.core.exceptions import NotFoundError
from app.models.document import Report
from app.repositories.analytics_repository import ReportRepository
from app.schemas.analytics import AnalyticsSummary, DepartmentSnapshot, ReportCreate
from app.services.compliance_service import ComplianceService
from app.services.finance_service import FinanceService
from app.services.manufacturing_service import ManufacturingService
from app.services.sales_service import SalesService


class AnalyticsService:
    """Cross-department BI layer. Rather than duplicating data into a
    warehouse table, this reads live from each department's existing
    service/summary — the same numbers each department page already
    shows, blended into one view for the CEO. Saved/scheduled reports use
    the `Report` model, which existed unmigrated since the Docs pass."""

    def __init__(self, db):
        self.db = db
        self.reports = ReportRepository(db)
        self.finance = FinanceService(db)
        self.sales = SalesService(db)
        self.manufacturing = ManufacturingService(db)
        self.compliance = ComplianceService(db)

    def list_reports(self, page: int, page_size: int, report_type: str | None = None):
        return self.reports.list(page=page, page_size=page_size, report_type=report_type)

    def get_report(self, report_id: str) -> Report:
        report = self.reports.get(report_id)
        if not report:
            raise NotFoundError("Report not found.")
        return report

    def create_report(self, data: ReportCreate, generated_by: str | None) -> Report:
        report = self.reports.create(Report(**data.model_dump(), generated_by=generated_by))

        # Building the cross-department summary and uploading it to object
        # storage is too slow for the request thread — the row comes back
        # immediately and s3_key fills in once the background task finishes.
        from app.tasks import safe_delay
        from app.tasks.reports import generate_report

        safe_delay(generate_report, report.id)
        return report

    def summary(self) -> AnalyticsSummary:
        finance = self.finance.summary()
        sales = self.sales.summary()
        manufacturing = self.manufacturing.summary()
        compliance = self.compliance.summary()

        snapshots = [
            DepartmentSnapshot(
                department="Finance",
                headline_metric="Net cash flow",
                headline_value=str(finance.net_cash_flow),
                secondary_metric="Burn rate",
                secondary_value=str(finance.burn_rate),
            ),
            DepartmentSnapshot(
                department="Sales",
                headline_metric="Open pipeline",
                headline_value=str(sales.total_pipeline_value),
                secondary_metric="Won deals",
                secondary_value=str(sales.won_deals),
            ),
            DepartmentSnapshot(
                department="Manufacturing",
                headline_metric="Avg yield rate",
                headline_value=f"{manufacturing.average_yield_rate}%",
                secondary_metric="Batches completed",
                secondary_value=str(manufacturing.completed),
            ),
            DepartmentSnapshot(
                department="Compliance",
                headline_metric="Compliance score",
                headline_value=f"{compliance.compliance_score}%",
                secondary_metric="Expired records",
                secondary_value=str(compliance.expired),
            ),
        ]

        return AnalyticsSummary(
            total_revenue=finance.total_revenue,
            total_expenses=finance.total_expenses,
            net_cash_flow=finance.net_cash_flow,
            open_pipeline_value=sales.total_pipeline_value,
            manufacturing_yield_rate=manufacturing.average_yield_rate,
            compliance_score=compliance.compliance_score,
            total_reports=self.reports.total_count(),
            snapshots=snapshots,
        )
