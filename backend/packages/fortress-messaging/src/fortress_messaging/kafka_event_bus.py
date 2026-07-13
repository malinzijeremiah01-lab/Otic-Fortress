"""Kafka-compatible producer used with Redpanda locally and Event Hubs in Azure."""

import json
from datetime import UTC, datetime
from typing import Any, Callable, Mapping

from .exceptions import (
    MessagePublishError,
    MessagingConfigurationError,
    MessagingDependencyError,
)
from .models import PublishResult


ProducerFactory = Callable[..., Any]


class KafkaEventBus:
    """Lazily managed ``aiokafka`` producer with JSON payloads and acknowledgements."""

    def __init__(
        self,
        bootstrap_servers: str,
        *,
        client_id: str = "fortress-messaging",
        producer_factory: ProducerFactory | None = None,
    ) -> None:
        if not bootstrap_servers.strip():
            raise MessagingConfigurationError("bootstrap_servers must not be empty")
        if not client_id.strip():
            raise MessagingConfigurationError("client_id must not be empty")
        self.bootstrap_servers = bootstrap_servers
        self.client_id = client_id
        self._producer_factory = producer_factory
        self._producer: Any | None = None
        self._started = False

    async def start(self) -> None:
        if self._started:
            return
        factory = self._producer_factory or self._load_producer_factory()
        self._producer = factory(
            bootstrap_servers=self.bootstrap_servers,
            client_id=self.client_id,
            acks="all",
            enable_idempotence=True,
            key_serializer=lambda key: key.encode("utf-8") if key is not None else None,
            value_serializer=lambda value: json.dumps(value, separators=(",", ":")).encode("utf-8"),
        )
        await self._producer.start()
        self._started = True

    async def publish(
        self,
        topic: str,
        key: str | None,
        value: Mapping[str, Any],
        *,
        headers: Mapping[str, str] | None = None,
    ) -> PublishResult:
        if not topic.strip():
            raise MessagingConfigurationError("topic must not be empty")
        if not isinstance(value, Mapping):
            raise MessagingConfigurationError("message value must be a mapping")
        if any(not isinstance(name, str) or not isinstance(content, str) for name, content in (headers or {}).items()):
            raise MessagingConfigurationError("message headers must be string pairs")
        await self.start()
        assert self._producer is not None
        encoded_headers = [(name, content.encode("utf-8")) for name, content in (headers or {}).items()]
        try:
            metadata = await self._producer.send_and_wait(
                topic, key=key, value=dict(value), headers=encoded_headers
            )
        except Exception as exc:
            raise MessagePublishError(f"Could not publish message to {topic!r}") from exc
        return PublishResult(
            topic=metadata.topic,
            partition=metadata.partition,
            offset=metadata.offset,
            timestamp=datetime.now(UTC),
        )

    async def close(self) -> None:
        if self._producer is not None and self._started:
            await self._producer.stop()
        self._producer = None
        self._started = False

    @staticmethod
    def _load_producer_factory() -> ProducerFactory:
        try:
            from aiokafka import AIOKafkaProducer
        except ImportError as exc:  # pragma: no cover - exercised only without package installation
            raise MessagingDependencyError(
                "aiokafka is required for KafkaEventBus; install fortress-messaging dependencies"
            ) from exc
        return AIOKafkaProducer
