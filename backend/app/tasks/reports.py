"""Background report-generation task.

Building a cross-department analytics snapshot and uploading it to object
storage is slow enough (several department services queried, then an S3
PUT) that it doesn't belong on the request thread: POST /analytics/reports
returns immediately with the Report row, and this task fills in the file
content (and s3_key) in the background.

Runs in a separate worker process, so it opens its own DB session
(SessionLocal) rather than reusing the request-scoped one from get_db.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

from app.core.logging import logger
from app.db.session import SessionLocal
from app.models.document import Report
from app.services.analytics_service import AnalyticsService
from app.storage import upload_bytes
from app.tasks.celery_app import celery_app


@celery_app.task(
    name="app.tasks.reports.generate_report",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True,
    max_retries=3,
)
def generate_report(report_id: str) -> None:
    db = SessionLocal()
    try:
        report = db.get(Report, report_id)
        if report is None:
            logger.warning("generate_report: report %s no longer exists; skipping.", report_id)
            return

        # Same cross-department numbers /analytics/summary already computes —
        # see AnalyticsService's docstring. Good enough as the report body
        # until per-department-filtered exports are needed.
        summary = AnalyticsService(db).summary()

        payload = {
            "report_id": report.id,
            "title": report.title,
            "report_type": report.report_type,
            "period_start": report.period_start,
            "period_end": report.period_end,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "summary": json.loads(summary.model_dump_json()),
        }
        content = json.dumps(payload, indent=2).encode("utf-8")

        stored_key = upload_bytes(f"reports/{report.id}.json", content, content_type="application/json")

        if stored_key:
            report.s3_key = stored_key
            db.commit()
            logger.info("Report %s generated and uploaded to %s.", report.id, stored_key)
        else:
            logger.info("Report %s generated but S3 isn't configured; s3_key left unset.", report.id)
    finally:
        db.close()
