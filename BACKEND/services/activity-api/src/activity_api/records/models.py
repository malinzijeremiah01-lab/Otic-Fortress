from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class ActivityRecordCreate(BaseModel):
    record_id: str
    tenant_id: str
    trace_id: str | None = None
    event_count: int = Field(ge=1)
    event_types: list[str] = Field(default_factory=list)
    first_occurred_at: datetime | None = None
    last_occurred_at: datetime | None = None
    events: list[dict[str, Any]] = Field(default_factory=list)
    summary: dict[str, int] = Field(default_factory=dict)


class ActivityRecord(ActivityRecordCreate):
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
