class LocalIdentityProvider:
    async def validate_token(self, token: str) -> dict:
        return {"sub": "local-user", "roles": ["admin"]}
