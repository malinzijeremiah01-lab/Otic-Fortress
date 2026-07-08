from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field

class EventEnvelope(BaseModel):
    event_id: str
    event_type: str
    schema_version: str = "1.0"
    tenant_id: str
    source_service: str
    occurred_at: datetime
    received_at: datetime | None = None
    trace_id: str | None = None
    span_id: str | None = None
    parent_span_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
