from fortress_events import is_supported_event_type


class SchemaValidator:
    def validate(self, event: dict) -> bool:
        if not isinstance(event, dict):
            return False

        required_fields = {"event_id", "tenant_id", "payload"}
        if not required_fields <= event.keys():
            return False

        if not isinstance(event["payload"], dict):
            return False

        return is_supported_event_type(event.get("event_type") or event.get("type"))
