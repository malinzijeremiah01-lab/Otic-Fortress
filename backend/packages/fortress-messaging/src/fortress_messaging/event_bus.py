"""Transport-independent producer contract."""

from typing import Any, Mapping, Protocol

from .models import PublishResult

class EventBus(Protocol):
    async def publish(
        self,
        topic: str,
        key: str | None,
        value: Mapping[str, Any],
        *,
        headers: Mapping[str, str] | None = None,
    ) -> PublishResult: ...

    async def close(self) -> None: ...
