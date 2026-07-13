from activity_api.records.models import ActivityRecord, ActivityRecordCreate
from activity_api.records.repository import ActivityRecordRepository


class ActivityRecordService:
    def __init__(self, repository: ActivityRecordRepository | None = None) -> None:
        self.repository = repository or ActivityRecordRepository()

    def create(self, payload: ActivityRecordCreate) -> ActivityRecord:
        record = ActivityRecord(**payload.model_dump())
        return self.repository.add(record)

    def get(self, record_id: str) -> ActivityRecord | None:
        return self.repository.get(record_id)

    def list(
        self,
        *,
        tenant_id: str | None = None,
        event_type: str | None = None,
        trace_id: str | None = None,
    ) -> list[ActivityRecord]:
        return self.repository.list(tenant_id=tenant_id, event_type=event_type, trace_id=trace_id)
