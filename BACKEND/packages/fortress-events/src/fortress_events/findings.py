from pydantic import BaseModel

class FindingPayload(BaseModel):
    finding_type: str
    severity: str
    summary: str
    entity_id: str | None = None
