class MockModelProvider:
    async def generate(self, prompt: str, context: dict | None = None) -> str:
        return "Mock explanation generated from recorded Fortress facts."
