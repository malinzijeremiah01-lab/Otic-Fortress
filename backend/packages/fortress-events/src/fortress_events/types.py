from enum import StrEnum


class EventType(StrEnum):
    MODEL_INVOCATION = "model_invocation"
    TOOL_INVOCATION = "tool_invocation"
    GOVERNANCE_DECISION = "governance_decision"
    ACTIVITY_RECORD_CREATED = "activity_record_created"
    FINDING_CREATED = "finding_created"
    AUDIT_EVENT = "audit_event"
    DEAD_LETTER_EVENT = "dead_letter_event"
    RAW_ARCHIVE_METADATA = "raw_archive_metadata"
    REPLAY_MANIFEST = "replay_manifest"
    UNIFIED_DECISION_RECORD = "unified_decision_record"
    UNKNOWN = "unknown"


EVENT_TYPE_ALIASES = {
    "model.invocation": EventType.MODEL_INVOCATION,
    "model-invocation": EventType.MODEL_INVOCATION,
    "modelInvocation": EventType.MODEL_INVOCATION,
    "tool.invocation": EventType.TOOL_INVOCATION,
    "tool-invocation": EventType.TOOL_INVOCATION,
    "toolInvocation": EventType.TOOL_INVOCATION,
    "governance.decision": EventType.GOVERNANCE_DECISION,
    "governance-decision": EventType.GOVERNANCE_DECISION,
    "governanceDecision": EventType.GOVERNANCE_DECISION,
    "activity.record.created": EventType.ACTIVITY_RECORD_CREATED,
    "activity-record-created": EventType.ACTIVITY_RECORD_CREATED,
    "finding.created": EventType.FINDING_CREATED,
    "finding-created": EventType.FINDING_CREATED,
    "audit.event": EventType.AUDIT_EVENT,
    "audit-event": EventType.AUDIT_EVENT,
    "dead.letter.event": EventType.DEAD_LETTER_EVENT,
    "dead-letter-event": EventType.DEAD_LETTER_EVENT,
    "raw.archive.metadata": EventType.RAW_ARCHIVE_METADATA,
    "raw-archive-metadata": EventType.RAW_ARCHIVE_METADATA,
    "replay.manifest": EventType.REPLAY_MANIFEST,
    "replay-manifest": EventType.REPLAY_MANIFEST,
    "unified.decision.record": EventType.UNIFIED_DECISION_RECORD,
    "unified-decision-record": EventType.UNIFIED_DECISION_RECORD,
}


CANONICAL_EVENT_TYPES = frozenset(event_type.value for event_type in EventType if event_type is not EventType.UNKNOWN)


def normalize_event_type(value: str | None) -> EventType:
    if value is None:
        return EventType.UNKNOWN

    stripped = value.strip()
    if not stripped:
        return EventType.UNKNOWN

    lowered = stripped.lower()
    snake_case = lowered.replace(".", "_").replace("-", "_")

    for candidate in (stripped, lowered, snake_case):
        if candidate in EVENT_TYPE_ALIASES:
            return EVENT_TYPE_ALIASES[candidate]
        try:
            return EventType(candidate)
        except ValueError:
            continue

    return EventType.UNKNOWN


def is_supported_event_type(value: str | None) -> bool:
    return normalize_event_type(value) is not EventType.UNKNOWN
