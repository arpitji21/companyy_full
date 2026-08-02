from app.core.exceptions import NotFoundError
from app.models.clinical import ClinicalEvent, ClinicalTrial
from app.repositories.clinical_repository import ClinicalEventRepository, ClinicalTrialRepository
from app.schemas.clinical import (
    ClinicalEventCreate,
    ClinicalSummary,
    ClinicalTrialCreate,
    ClinicalTrialUpdate,
)


class ClinicalService:
    def __init__(self, db):
        self.db = db
        self.trials = ClinicalTrialRepository(db)
        self.events = ClinicalEventRepository(db)

    def list_trials(self, page: int, page_size: int, status: str | None = None, phase: str | None = None):
        return self.trials.list(page=page, page_size=page_size, status=status, phase=phase)

    def get_trial(self, trial_id: str) -> ClinicalTrial:
        trial = self.trials.get(trial_id)
        if not trial:
            raise NotFoundError("Clinical trial not found.")
        return trial

    def create_trial(self, data: ClinicalTrialCreate) -> ClinicalTrial:
        return self.trials.create(ClinicalTrial(**data.model_dump()))

    def update_trial(self, trial_id: str, data: ClinicalTrialUpdate) -> ClinicalTrial:
        trial = self.get_trial(trial_id)
        return self.trials.update(trial, data.model_dump(exclude_unset=True))

    def list_events(self, page: int, page_size: int, trial_id: str | None = None, event_type: str | None = None):
        return self.events.list(page=page, page_size=page_size, trial_id=trial_id, event_type=event_type)

    def create_event(self, data: ClinicalEventCreate) -> ClinicalEvent:
        return self.events.create(ClinicalEvent(**data.model_dump()))

    def summary(self) -> ClinicalSummary:
        by_status = self.trials.counts_by_status()
        target, actual = self.trials.enrollment_totals()
        return ClinicalSummary(
            total_trials=sum(by_status.values()),
            active_trials=by_status.get("active", 0) + by_status.get("recruiting", 0),
            completed_trials=by_status.get("completed", 0),
            total_target_enrollment=target,
            total_actual_enrollment=actual,
            enrollment_rate=round((actual / target * 100), 1) if target else 0.0,
            open_adverse_events=self.events.open_count_by_type("adverse_event"),
            open_protocol_deviations=self.events.open_count_by_type("protocol_deviation"),
        )
