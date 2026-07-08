from pydantic import BaseModel

class PolicyRule(BaseModel):
    name: str
    condition: str
    effect: str

class PolicyDocument(BaseModel):
    policy_id: str
    version: str
    default_effect: str = "deny"
    rules: list[PolicyRule] = []
