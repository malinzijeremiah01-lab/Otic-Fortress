from pydantic import BaseModel

class Settings(BaseModel):
    service_name: str = "ingestion-api"
    raw_topic: str = "fortress.raw.telemetry"
    kafka_bootstrap_servers: str = "localhost:19092"

settings = Settings()
