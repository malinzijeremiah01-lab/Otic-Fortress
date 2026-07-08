class AzureBlobObjectStorage:
    """Future Azure adapter. Keep Azure SDK usage isolated here."""
    async def put_object(self, bucket: str, key: str, data: bytes) -> str:
        return f"azure-blob://{bucket}/{key}"
    async def get_object(self, bucket: str, key: str) -> bytes:
        return b""
