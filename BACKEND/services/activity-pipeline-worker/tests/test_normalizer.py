from activity_pipeline_worker.normalization.normalizer import Normalizer


def test_normalizer_canonicalizes_event_type_alias():
    normalized = Normalizer().normalize(
        {
            "event_id": "evt_1",
            "type": "model.invocation",
            "tenant_id": "tenant_1",
            "source_service": "sdk",
            "trace_id": "trace_1",
            "payload": {"model_provider": "openai", "model_name": "gpt-4.1"},
        }
    )

    assert normalized["event_type"] == "model_invocation"
    assert normalized["event_id"] == "evt_1"
    assert normalized["tenant_id"] == "tenant_1"
    assert normalized["trace_id"] == "trace_1"


def test_normalizer_infers_tool_invocation_from_payload():
    normalized = Normalizer().normalize(
        {
            "event_id": "evt_2",
            "tenant_id": "tenant_1",
            "payload": {"tool_name": "search", "action_name": "query"},
        }
    )

    assert normalized["event_type"] == "tool_invocation"
