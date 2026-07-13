from activity_api.records.models import ActivityRecord


class ActivityRecordRepository:
    def __init__(self) -> None:
        self._records: dict[str, ActivityRecord] = {}

    def add(self, record: ActivityRecord) -> ActivityRecord:
        self._records[record.record_id] = record
        return record

    def get(self, record_id: str) -> ActivityRecord | None:
        return self._records.get(record_id)

    def list(
        self,
        *,
        tenant_id: str | None = None,
        event_type: str | None = None,
        trace_id: str | None = None,
    ) -> list[ActivityRecord]:
        records = list(self._records.values())
        if tenant_id is not None:
            records = [record for record in records if record.tenant_id == tenant_id]
        if event_type is not None:
            records = [record for record in records if event_type in record.event_types]
        if trace_id is not None:
            records = [record for record in records if record.trace_id == trace_id]
        return sorted(records, key=lambda record: record.created_at, reverse=True)
