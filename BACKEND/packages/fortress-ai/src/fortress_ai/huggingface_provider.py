class HuggingFaceProvider:
    """Development/provider abstraction placeholder. Do not send sensitive data unless approved."""
    async def generate(self, prompt: str, context: dict | None = None) -> str:
        raise NotImplementedError
