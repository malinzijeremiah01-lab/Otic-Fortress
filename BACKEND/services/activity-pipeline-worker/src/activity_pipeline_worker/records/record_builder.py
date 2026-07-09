from collections import defaultdict
from datetime import UTC, datetime
from typing import Any


class RecordBuilder:
    def build(self, events: list[dict]) -> dict:
        if not events:
            raise ValueError("Cannot build an activity record without events.")

        tenant_ids = {event["tenant_id"] for event in events}
        if len(tenant_ids) != 1:
            raise ValueError("All events in an activity record must belong to the same tenant.")

        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for event in events:
            grouped[event["event_type"]].append(event)

        first_event = events[0]
        occurred_values = [event.get("occurred_at") for event in events if event.get("occurred_at")]

        return {
            "record_id": f"activity_{first_event['event_id']}",
            "tenant_id": first_event["tenant_id"],
            "trace_id": first_event.get("trace_id"),
            "event_count": len(events),
            "event_types": sorted(grouped.keys()),
            "first_occurred_at": min(occurred_values) if occurred_values else None,
            "last_occurred_at": max(occurred_values) if occurred_values else None,
            "created_at": datetime.now(UTC).isoformat(),
            "events": events,
            "summary": self._summarize(grouped),
        }

    def _summarize(self, grouped: dict[str, list[dict[str, Any]]]) -> dict[str, int]:
        return {event_type: len(events) for event_type, events in grouped.items()}
