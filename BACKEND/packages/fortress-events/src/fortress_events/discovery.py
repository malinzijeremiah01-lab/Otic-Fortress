from pydantic import BaseModel

class DiscoveryPayload(BaseModel):
    observed_entity: str
    entity_type: str
    confidence: float
    source: str
