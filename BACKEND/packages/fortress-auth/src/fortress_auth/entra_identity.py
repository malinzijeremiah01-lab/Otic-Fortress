class EntraIdentityProvider:
    """Future Entra adapter."""
    async def validate_token(self, token: str) -> dict:
        raise NotImplementedError("Entra validation is added when Azure access is available")
