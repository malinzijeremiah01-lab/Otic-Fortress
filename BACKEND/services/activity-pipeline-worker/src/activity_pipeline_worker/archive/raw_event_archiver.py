class RawEventArchiver:
    async def archive(self, event: dict) -> str:
        return "raw-events/local/event.json"
