from pydantic import BaseModel

class ToolInvocationPayload(BaseModel):
    agent_id: str
    tool_name: str
    tool_type: str
    action_name: str
    input_hash: str | None = None
    output_hash: str | None = None
