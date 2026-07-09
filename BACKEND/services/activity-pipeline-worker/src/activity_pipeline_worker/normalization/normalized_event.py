from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

class NormalizedEvent(BaseModel):
    event_id: str
    event_type: str
    tenant_id: str
    source_service: str | None = None
    occurred_at: datetime | None = None
    trace_id: str | None = None
    span_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
