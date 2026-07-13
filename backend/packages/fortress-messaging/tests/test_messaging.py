import asyncio
from types import SimpleNamespace

import pytest

from fortress_messaging import EventPublisher, InMemoryEventBus, KafkaEventBus
from fortress_messaging.consumer import KafkaEventConsumer
from fortress_messaging.exceptions import MessagingConfigurationError, MessagePublishError


def test_event_publisher_returns_broker_neutral_acknowledgement():
    async def scenario():
        bus = InMemoryEventBus()
        result = await EventPublisher(bus).publish(
            "fortress.normalized.events", "tenant-1", {"event_id": "event-1"}, headers={"trace-id": "t1"}
        )

        assert result.topic == "fortress.normalized.events"
        assert result.offset == 0
        assert bus.messages[0].key == "tenant-1"
        assert bus.messages[0].headers == {"trace-id": "t1"}

    asyncio.run(scenario())


def test_in_memory_bus_rejects_publishing_after_close():
    async def scenario():
        bus = InMemoryEventBus()
        await bus.close()
        with pytest.raises(MessagingConfigurationError, match="closed"):
            await bus.publish("fortress.findings", None, {"id": "finding-1"})

    asyncio.run(scenario())


def test_kafka_bus_starts_once_serializes_messages_and_stops():
    class FakeProducer:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.started = 0
            self.stopped = 0
            self.sent = []

        async def start(self):
            self.started += 1

        async def send_and_wait(self, topic, **kwargs):
            self.sent.append((topic, kwargs))
            return SimpleNamespace(topic=topic, partition=2, offset=9)

        async def stop(self):
            self.stopped += 1

    instances = []

    def factory(**kwargs):
        producer = FakeProducer(**kwargs)
        instances.append(producer)
        return producer

    async def scenario():
        bus = KafkaEventBus("localhost:19092", producer_factory=factory)
        result = await bus.publish("fortress.findings", "tenant-1", {"severity": "high"})
        await bus.publish("fortress.findings", "tenant-1", {"severity": "low"})
        await bus.close()

        assert result.partition == 2
        assert result.offset == 9

    asyncio.run(scenario())
    producer = instances[0]
    assert producer.started == 1
    assert producer.stopped == 1
    assert producer.kwargs["acks"] == "all"
    assert producer.kwargs["value_serializer"]({"ok": True}) == b'{"ok":true}'


def test_kafka_bus_wraps_broker_publish_failures():
    class FailingProducer:
        async def start(self):
            pass

        async def send_and_wait(self, *args, **kwargs):
            raise RuntimeError("broker unavailable")

        async def stop(self):
            pass

    async def scenario():
        bus = KafkaEventBus("localhost:19092", producer_factory=lambda **kwargs: FailingProducer())
        with pytest.raises(MessagePublishError, match="fortress.findings"):
            await bus.publish("fortress.findings", None, {"id": "finding-1"})

    asyncio.run(scenario())


def test_consumer_delivers_message_then_commits_offset():
    observed = []

    async def handler(message):
        observed.append(message)

    class FakeConsumer:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self.started = False
            self.stopped = False
            self.commits = 0
            self._messages = [
                SimpleNamespace(
                    topic="fortress.normalized.events",
                    key="tenant-1",
                    value={"event_id": "event-1"},
                    headers=[("trace-id", b"trace-1")],
                    partition=1,
                    offset=5,
                    timestamp=0,
                )
            ]

        async def start(self):
            self.started = True

        async def stop(self):
            self.stopped = True

        async def commit(self):
            self.commits += 1

        def __aiter__(self):
            return self._iterator()

        async def _iterator(self):
            for message in self._messages:
                yield message

    instances = []

    def factory(*topics, **kwargs):
        consumer = FakeConsumer(**kwargs)
        instances.append(consumer)
        return consumer

    async def scenario():
        consumer = KafkaEventConsumer(
            "localhost:19092", ["fortress.normalized.events"], "activity-worker", handler, consumer_factory=factory
        )
        await consumer.run()
        await consumer.close()

    asyncio.run(scenario())
    assert observed[0].headers == {"trace-id": "trace-1"}
    assert observed[0].offset == 5
    assert instances[0].commits == 1
    assert instances[0].kwargs["enable_auto_commit"] is False


def test_consumer_requires_an_async_handler():
    with pytest.raises(MessagingConfigurationError, match="async"):
        KafkaEventConsumer("localhost:19092", ["fortress.findings"], "worker", lambda message: None)
