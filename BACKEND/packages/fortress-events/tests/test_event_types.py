from fortress_events import EventType, is_supported_event_type, normalize_event_type


def test_normalize_event_type_accepts_canonical_values():
    assert normalize_event_type("model_invocation") is EventType.MODEL_INVOCATION


def test_normalize_event_type_accepts_common_aliases():
    assert normalize_event_type("tool.invocation") is EventType.TOOL_INVOCATION
    assert normalize_event_type("governance-decision") is EventType.GOVERNANCE_DECISION


def test_is_supported_event_type_rejects_unknown_values():
    assert is_supported_event_type("unknown_event") is False
    assert is_supported_event_type(None) is False
