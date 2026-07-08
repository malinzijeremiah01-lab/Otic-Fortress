class EvidenceWriter:
    async def write(self, record: dict) -> str:
        return "evidence://local"
