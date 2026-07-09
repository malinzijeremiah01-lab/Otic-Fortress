import pytest

from activity_pipeline_worker.records.record_builder import RecordBuilder


def test_record_builder_groups_events_into_activity_record():
    record = RecordBuilder().build(
        [
            {
                "event_id": "evt_1",
                "event_type": "model_invocation",
                "tenant_id": "tenant_1",
                "trace_id": "trace_1",
                "occurred_at": "2026-07-09T10:00:00Z",
                "payload": {},
            },
            {
                "event_id": "evt_2",
                "event_type": "tool_invocation",
                "tenant_id": "tenant_1",
                "trace_id": "trace_1",
                "occurred_at": "2026-07-09T10:01:00Z",
                "payload": {},
            },
        ]
    )

    assert record["record_id"] == "activity_evt_1"
    assert record["tenant_id"] == "tenant_1"
    assert record["trace_id"] == "trace_1"
    assert record["event_count"] == 2
    assert record["event_types"] == ["model_invocation", "tool_invocation"]
    assert record["summary"] == {"model_invocation": 1, "tool_invocation": 1}


def test_record_builder_rejects_cross_tenant_records():
    with pytest.raises(ValueError, match="same tenant"):
        RecordBuilder().build(
            [
                {"event_id": "evt_1", "event_type": "model_invocation", "tenant_id": "tenant_1"},
                {"event_id": "evt_2", "event_type": "tool_invocation", "tenant_id": "tenant_2"},
            ]
        )
