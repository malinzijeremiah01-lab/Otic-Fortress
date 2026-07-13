"""Application-facing event publishing service."""

from typing import Any, Mapping

from .event_bus import EventBus
from .models import PublishResult

class EventPublisher:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def publish(
        self,
        topic: str,
        key: str | None,
        event: Mapping[str, Any],
        *,
        headers: Mapping[str, str] | None = None,
    ) -> PublishResult:
        """Publish an event without exposing a broker-specific API to services."""
        return await self.event_bus.publish(topic, key, event, headers=headers)
