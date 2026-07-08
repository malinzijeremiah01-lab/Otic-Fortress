from pydantic import BaseModel

class ModelInvocationPayload(BaseModel):
    agent_id: str
    model_provider: str
    model_name: str
    prompt_hash: str | None = None
    output_hash: str | None = None
