class RecordBuilder:
    def build(self, events: list[dict]) -> dict:
        return {"events": events}
