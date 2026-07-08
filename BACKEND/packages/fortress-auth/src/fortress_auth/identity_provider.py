from typing import Protocol

class IdentityProvider(Protocol):
    async def validate_token(self, token: str) -> dict: ...
