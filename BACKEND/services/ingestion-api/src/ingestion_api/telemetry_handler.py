async def accept_telemetry(event: dict) -> bool:
    # V1: validate envelope lightly and publish to raw topic through fortress-messaging adapter.
    return True
