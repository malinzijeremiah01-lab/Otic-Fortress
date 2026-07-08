from pydantic import BaseModel

class ServiceSettings(BaseModel):
    service_name: str
    environment: str = "local"
