from pydantic import BaseModel

class NormalizedEvent(BaseModel):
    event_id: str
    event_type: str
    tenant_id: str
    trace_id: str | None = None
    payload: dict = {}
