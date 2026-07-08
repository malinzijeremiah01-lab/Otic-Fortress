from pydantic import BaseModel

class ObjectRef(BaseModel):
    uri: str
    content_type: str | None = None
    sha256: str | None = None
