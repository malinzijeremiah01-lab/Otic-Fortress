from fortress_events import EventType, normalize_event_type


class EventTypeClassifier:
    def classify(self, event: dict) -> str:
        event_type = event.get("event_type") or event.get("type")
        payload = event.get("payload") or {}

        normalized = normalize_event_type(event_type)
        if normalized is not EventType.UNKNOWN:
            return normalized.value

        if {"model_provider", "model_name"} <= payload.keys():
            return EventType.MODEL_INVOCATION.value
        if {"tool_name", "action_name"} <= payload.keys():
            return EventType.TOOL_INVOCATION.value
        if {"decision", "policy_id"} & payload.keys():
            return EventType.GOVERNANCE_DECISION.value

        return EventType.UNKNOWN.value
