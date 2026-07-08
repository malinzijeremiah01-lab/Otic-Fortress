from typing import Protocol

class ModelProvider(Protocol):
    async def generate(self, prompt: str, context: dict | None = None) -> str: ...
