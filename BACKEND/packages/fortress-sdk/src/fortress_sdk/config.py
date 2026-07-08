from pydantic import BaseModel

class FortressSDKConfig(BaseModel):
    tenant_id: str
    agent_id: str
    ingestion_url: str = "http://localhost:8001/v1/telemetry"
