from uuid import uuid4

def new_id(prefix: str = "") -> str:
    value = str(uuid4())
    return f"{prefix}_{value}" if prefix else value
