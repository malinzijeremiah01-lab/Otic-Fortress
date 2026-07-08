from typing import Any

class KafkaEventBus:
    """Kafka-compatible event bus adapter.

    Local: Redpanda.
    Future Azure: Event Hubs Kafka endpoint.
    """
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers

    async def publish(self, topic: str, key: str | None, value: dict[str, Any]) -> None:
        # Placeholder: wire aiokafka after contracts stabilize.
        return None

    async def close(self) -> None:
        return None
