"""Exceptions that callers can use to distinguish messaging failures."""


class MessagingError(Exception):
    """Base exception for fortress-messaging."""


class MessagingConfigurationError(MessagingError, ValueError):
    """Messaging was configured with invalid values."""


class MessagingDependencyError(MessagingError, RuntimeError):
    """An optional broker client dependency is not installed."""


class MessagePublishError(MessagingError):
    """The broker did not acknowledge a publish."""
