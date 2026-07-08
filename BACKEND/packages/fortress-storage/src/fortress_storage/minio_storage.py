class MinioObjectStorage:
    async def put_object(self, bucket: str, key: str, data: bytes) -> str:
        return f"minio://{bucket}/{key}"
    async def get_object(self, bucket: str, key: str) -> bytes:
        return b""
