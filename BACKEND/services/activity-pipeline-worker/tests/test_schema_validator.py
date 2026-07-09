from activity_pipeline_worker.validation.schema_validator import SchemaValidator


def test_schema_validator_accepts_supported_event():
    event = {
        "event_id": "evt_1",
        "event_type": "model_invocation",
        "tenant_id": "tenant_1",
        "payload": {"model_provider": "openai", "model_name": "gpt-4.1"},
    }

    assert SchemaValidator().validate(event) is True


def test_schema_validator_rejects_missing_required_fields():
    assert SchemaValidator().validate({"event_type": "model_invocation"}) is False


def test_schema_validator_rejects_unknown_event_type():
    event = {
        "event_id": "evt_1",
        "event_type": "made_up_event",
        "tenant_id": "tenant_1",
        "payload": {},
    }

    assert SchemaValidator().validate(event) is False
