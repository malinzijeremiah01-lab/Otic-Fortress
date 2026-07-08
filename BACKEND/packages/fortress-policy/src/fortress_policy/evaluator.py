from .decisions import PolicyDecision
from .models import PolicyDocument

class PolicyEvaluator:
    def evaluate(self, policy: PolicyDocument, context: dict) -> tuple[PolicyDecision, str]:
        # V1 placeholder: real condition engine comes after event contracts stabilize.
        return PolicyDecision(policy.default_effect), "default policy effect applied"
