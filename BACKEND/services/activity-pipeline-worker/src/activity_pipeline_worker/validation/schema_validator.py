class SchemaValidator:
    def validate(self, event: dict) -> bool:
        return "event_type" in event or "payload" in event
