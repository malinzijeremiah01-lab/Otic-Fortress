from fastapi import APIRouter, HTTPException, Query, status

from activity_api.records.models import ActivityRecord, ActivityRecordCreate
from activity_api.records.service import ActivityRecordService

router = APIRouter(prefix="/v1/activity-records", tags=["activity-records"])
service = ActivityRecordService()


@router.post("/", response_model=ActivityRecord, status_code=status.HTTP_201_CREATED)
def create_record(payload: ActivityRecordCreate) -> ActivityRecord:
    return service.create(payload)


@router.get("/", response_model=list[ActivityRecord])
def list_records(
    tenant_id: str | None = Query(default=None),
    event_type: str | None = Query(default=None),
    trace_id: str | None = Query(default=None),
) -> list[ActivityRecord]:
    return service.list(tenant_id=tenant_id, event_type=event_type, trace_id=trace_id)


@router.get("/{record_id}", response_model=ActivityRecord)
def get_record(record_id: str) -> ActivityRecord:
    record = service.get(record_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity record not found.")
    return record
