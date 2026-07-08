from pydantic import BaseModel

class DeadLetterPayload(BaseModel):
    original_event_id: str | None = None
    reason: str
    details: str | None = None
    raw_payload_ref: str | None = None
