class EventTypeClassifier:
    def classify(self, event: dict) -> str:
        return event.get("event_type", "unknown")
