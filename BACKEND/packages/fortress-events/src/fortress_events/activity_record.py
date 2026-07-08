from typing import Any
from pydantic import BaseModel, Field

class UnifiedDecisionRecord(BaseModel):
    decision_id: str
    tenant_id: str
    trace_id: str | None = None
    agent_id: str | None = None
    user_id: str | None = None
    model_id: str | None = None
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    policy_evaluations: list[dict[str, Any]] = Field(default_factory=list)
    enforcement_decisions: list[dict[str, Any]] = Field(default_factory=list)
    approvals: list[dict[str, Any]] = Field(default_factory=list)
    risk_signals: list[dict[str, Any]] = Field(default_factory=list)
    anomaly_findings: list[dict[str, Any]] = Field(default_factory=list)
    evidence_hash: str | None = None
