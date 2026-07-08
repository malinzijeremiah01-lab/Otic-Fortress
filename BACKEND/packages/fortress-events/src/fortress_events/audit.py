from pydantic import BaseModel

class AuditEventPayload(BaseModel):
    record_id: str
    record_type: str
    previous_hash: str | None = None
    current_hash: str
