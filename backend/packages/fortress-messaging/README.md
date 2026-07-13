# fortress-messaging

Shared, Kafka-compatible messaging primitives for Otic Fortress backend services.

The package provides `EventPublisher`, `KafkaEventBus`, `KafkaEventConsumer`, canonical `Topic` names, and `InMemoryEventBus` for unit tests. See the [backend events and messaging architecture](../../docs/events-and-messaging.md) for topic ownership, delivery semantics, and integration examples.
