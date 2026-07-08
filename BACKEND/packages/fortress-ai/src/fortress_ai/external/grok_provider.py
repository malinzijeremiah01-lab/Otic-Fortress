class GrokProvider:
    """External API provider for development/demo only.

    Do not use for regulated production payloads, PII, secrets, or customer data.
    """
    async def generate(self, prompt: str, context: dict | None = None) -> str:
        raise NotImplementedError("Grok provider requires explicit dev-only configuration")
