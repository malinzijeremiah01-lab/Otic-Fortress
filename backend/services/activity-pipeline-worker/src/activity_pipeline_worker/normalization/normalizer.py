from activity_pipeline_worker.classification.event_type_classifier import EventTypeClassifier
from activity_pipeline_worker.normalization.normalized_event import NormalizedEvent


class Normalizer:
    def __init__(self, classifier: EventTypeClassifier | None = None) -> None:
        self.classifier = classifier or EventTypeClassifier()

    def normalize(self, event: dict) -> dict:
        normalized = NormalizedEvent(
            event_id=event["event_id"],
            event_type=self.classifier.classify(event),
            tenant_id=event["tenant_id"],
            source_service=event.get("source_service"),
            occurred_at=event.get("occurred_at"),
            trace_id=event.get("trace_id"),
            span_id=event.get("span_id"),
            payload=event.get("payload") or {},
        )
        return normalized.model_dump(mode="json")
