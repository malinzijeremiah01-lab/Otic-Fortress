"""Reliable, broker-neutral messaging primitives for Otic Fortress services."""

from .consumer import KafkaEventConsumer
from .event_bus import EventBus
from .in_memory import InMemoryEventBus
from .kafka_event_bus import KafkaEventBus
from .models import ConsumedMessage, PublishResult
from .publisher import EventPublisher
from .topics import ALL_TOPICS, Topic

__all__ = [
    "ALL_TOPICS",
    "ConsumedMessage",
    "EventBus",
    "EventPublisher",
    "InMemoryEventBus",
    "KafkaEventBus",
    "KafkaEventConsumer",
    "PublishResult",
    "Topic",
]
