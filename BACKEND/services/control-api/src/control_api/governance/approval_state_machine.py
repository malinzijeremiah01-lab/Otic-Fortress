from enum import StrEnum

class ApprovalState(StrEnum):
    REQUESTED = "requested"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"
    ESCALATED = "escalated"
    CANCELLED = "cancelled"

ALLOWED_TRANSITIONS = {
    ApprovalState.REQUESTED: {ApprovalState.PENDING_REVIEW, ApprovalState.CANCELLED},
    ApprovalState.PENDING_REVIEW: {ApprovalState.APPROVED, ApprovalState.DENIED, ApprovalState.EXPIRED, ApprovalState.ESCALATED},
    ApprovalState.ESCALATED: {ApprovalState.APPROVED, ApprovalState.DENIED, ApprovalState.EXPIRED},
}

def transition(current: ApprovalState, target: ApprovalState) -> ApprovalState:
    if target not in ALLOWED_TRANSITIONS.get(current, set()):
        raise ValueError(f"Invalid approval transition: {current} -> {target}")
    return target
