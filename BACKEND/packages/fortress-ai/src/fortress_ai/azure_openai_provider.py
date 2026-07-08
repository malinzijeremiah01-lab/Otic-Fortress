class AzureOpenAIProvider:
    """Future approved enterprise provider adapter."""
    async def generate(self, prompt: str, context: dict | None = None) -> str:
        raise NotImplementedError("Azure OpenAI adapter is implemented when Azure access is available")
