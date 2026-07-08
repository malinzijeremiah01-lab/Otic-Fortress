from typing import Literal
from pydantic import BaseModel

class GovernanceDecisionPayload(BaseModel):
    agent_id: str
    tool_name: str | None = None
    action_name: str | None = None
    policy_id: str | None = None
    policy_version: str | None = None
    decision: Literal["allow", "deny", "require_approval", "redact"]
    reason: str
    risk_level: Literal["low", "medium", "high", "critical"] = "low"
