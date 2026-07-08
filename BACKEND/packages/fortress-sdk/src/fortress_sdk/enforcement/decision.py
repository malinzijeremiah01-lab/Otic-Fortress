from enum import StrEnum

class EnforcementDecision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"
    REDACT = "redact"
