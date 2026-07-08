from .event_bus import EventBus

class EventPublisher:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def publish(self, topic: str, key: str | None, event: dict) -> None:
        await self.event_bus.publish(topic, key, event)
