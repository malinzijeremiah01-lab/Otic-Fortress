from functools import wraps
from .decision import EnforcementDecision


def govern_tool(config, tool_name: str, tool_type: str):
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            decision = EnforcementDecision.ALLOW
            # V1 placeholder emits telemetry later.
            if decision == EnforcementDecision.ALLOW:
                return fn(*args, **kwargs)
            raise RuntimeError(f"Tool {tool_name} blocked by Fortress")
        return wrapped
    return decorator
