"""Broker-neutral message models returned to backend services."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class PublishResult:
    """Broker acknowledgement for a successfully published message."""

    topic: str
    partition: int | None = None
    offset: int | None = None
    timestamp: datetime | None = None


@dataclass(frozen=True, slots=True)
class ConsumedMessage:
    """A decoded broker message delivered to an application handler."""

    topic: str
    value: Mapping[str, Any]
    key: str | None = None
    headers: Mapping[str, str] | None = None
    partition: int | None = None
    offset: int | None = None
    timestamp: datetime | None = None
