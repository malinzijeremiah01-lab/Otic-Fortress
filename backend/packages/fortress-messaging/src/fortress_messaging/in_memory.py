"""Deterministic broker substitute for unit tests and local application wiring."""

from datetime import UTC, datetime
from typing import Any, Mapping

from .exceptions import MessagingConfigurationError
from .models import ConsumedMessage, PublishResult


class InMemoryEventBus:
    """Captures published messages without pretending to be a durable broker."""

    def __init__(self) -> None:
        self.messages: list[ConsumedMessage] = []
        self.closed = False

    async def publish(
        self,
        topic: str,
        key: str | None,
        value: Mapping[str, Any],
        *,
        headers: Mapping[str, str] | None = None,
    ) -> PublishResult:
        if self.closed:
            raise MessagingConfigurationError("event bus is closed")
        if not topic.strip():
            raise MessagingConfigurationError("topic must not be empty")
        if not isinstance(value, Mapping):
            raise MessagingConfigurationError("message value must be a mapping")
        timestamp = datetime.now(UTC)
        offset = len(self.messages)
        self.messages.append(
            ConsumedMessage(
                topic=topic,
                key=key,
                value=dict(value),
                headers=dict(headers or {}),
                partition=0,
                offset=offset,
                timestamp=timestamp,
            )
        )
        return PublishResult(topic=topic, partition=0, offset=offset, timestamp=timestamp)

    async def close(self) -> None:
        self.closed = True
