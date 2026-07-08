from .config import FortressSDKConfig
from .enforcement.wrapper import govern_tool

class FortressClient:
    def __init__(self, tenant_id: str, agent_id: str, ingestion_url: str = "http://localhost:8001/v1/telemetry"):
        self.config = FortressSDKConfig(tenant_id=tenant_id, agent_id=agent_id, ingestion_url=ingestion_url)

    def govern_tool(self, tool_name: str, tool_type: str = "generic"):
        return govern_tool(self.config, tool_name, tool_type)
