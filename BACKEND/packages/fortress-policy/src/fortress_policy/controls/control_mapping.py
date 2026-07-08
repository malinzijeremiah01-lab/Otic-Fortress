from pydantic import BaseModel

class ControlMapping(BaseModel):
    control_id: str
    framework: str
    description: str
