"""Canonical broker topics owned by the backend."""

from enum import StrEnum


class Topic(StrEnum):
    RAW_TELEMETRY = "fortress.raw.telemetry"
    NORMALIZED_EVENTS = "fortress.normalized.events"
    ACTIVITY_RECORDS = "fortress.activity.records"
    FINDINGS = "fortress.findings"
    AUDIT_EVENTS = "fortress.audit.events"
    DLQ_TELEMETRY = "fortress.dlq.telemetry"
    DLQ_TRANSFORMATION = "fortress.dlq.transformation"
    REPLAY_TELEMETRY = "fortress.replay.telemetry"


RAW_TELEMETRY = Topic.RAW_TELEMETRY
NORMALIZED_EVENTS = Topic.NORMALIZED_EVENTS
ACTIVITY_RECORDS = Topic.ACTIVITY_RECORDS
FINDINGS = Topic.FINDINGS
AUDIT_EVENTS = Topic.AUDIT_EVENTS
DLQ_TELEMETRY = Topic.DLQ_TELEMETRY
DLQ_TRANSFORMATION = Topic.DLQ_TRANSFORMATION
REPLAY_TELEMETRY = Topic.REPLAY_TELEMETRY

ALL_TOPICS = frozenset(topic.value for topic in Topic)
