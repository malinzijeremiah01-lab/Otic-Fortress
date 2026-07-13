"""Kafka-compatible consumer with explicit at-least-once processing semantics."""

import inspect
import json
from datetime import UTC, datetime
from typing import Any, Awaitable, Callable, Iterable, Mapping

from .exceptions import MessagingConfigurationError, MessagingDependencyError
from .models import ConsumedMessage


MessageHandler = Callable[[ConsumedMessage], Awaitable[None]]
ConsumerFactory = Callable[..., Any]


class KafkaEventConsumer:
    """Consume JSON object messages and hand them to an async service handler.

    Offsets are committed by the broker client only after the handler succeeds. If
    a handler raises, the error intentionally propagates so deployment supervision
    can restart the worker and the message remains eligible for redelivery.
    """

    def __init__(
        self,
        bootstrap_servers: str,
        topics: Iterable[str],
        group_id: str,
        handler: MessageHandler,
        *,
        client_id: str = "fortress-messaging",
        consumer_factory: ConsumerFactory | None = None,
    ) -> None:
        normalized_topics = tuple(dict.fromkeys(topic for topic in topics if isinstance(topic, str) and topic.strip()))
        if not bootstrap_servers.strip():
            raise MessagingConfigurationError("bootstrap_servers must not be empty")
        if not normalized_topics:
            raise MessagingConfigurationError("at least one topic is required")
        if not group_id.strip():
            raise MessagingConfigurationError("group_id must not be empty")
        if not inspect.iscoroutinefunction(handler):
            raise MessagingConfigurationError("handler must be an async callable")
        self.bootstrap_servers = bootstrap_servers
        self.topics = normalized_topics
        self.group_id = group_id
        self.handler = handler
        self.client_id = client_id
        self._consumer_factory = consumer_factory
        self._consumer: Any | None = None
        self._started = False

    async def start(self) -> None:
        if self._started:
            return
        factory = self._consumer_factory or self._load_consumer_factory()
        self._consumer = factory(
            *self.topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            client_id=self.client_id,
            enable_auto_commit=False,
            auto_offset_reset="earliest",
            key_deserializer=lambda key: key.decode("utf-8") if key is not None else None,
            value_deserializer=lambda value: json.loads(value.decode("utf-8")),
        )
        await self._consumer.start()
        self._started = True

    async def run(self) -> None:
        """Run until cancelled; callers should always close this consumer on shutdown."""
        await self.start()
        assert self._consumer is not None
        async for message in self._consumer:
            if not isinstance(message.value, Mapping):
                raise MessagingConfigurationError("consumed message value must be a JSON object")
            headers = {
                name: content.decode("utf-8")
                for name, content in (message.headers or [])
                if content is not None
            }
            timestamp = (
                datetime.fromtimestamp(message.timestamp / 1000, UTC)
                if message.timestamp is not None
                else None
            )
            await self.handler(
                ConsumedMessage(
                    topic=message.topic,
                    key=message.key,
                    value=dict(message.value),
                    headers=headers,
                    partition=message.partition,
                    offset=message.offset,
                    timestamp=timestamp,
                )
            )
            await self._consumer.commit()

    async def close(self) -> None:
        if self._consumer is not None and self._started:
            await self._consumer.stop()
        self._consumer = None
        self._started = False

    @staticmethod
    def _load_consumer_factory() -> ConsumerFactory:
        try:
            from aiokafka import AIOKafkaConsumer
        except ImportError as exc:  # pragma: no cover - exercised only without package installation
            raise MessagingDependencyError(
                "aiokafka is required for KafkaEventConsumer; install fortress-messaging dependencies"
            ) from exc
        return AIOKafkaConsumer
