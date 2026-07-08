class FortressError(Exception):
    """Base Fortress error."""

class ValidationFailure(FortressError):
    """Raised when a contract or semantic validation fails."""
