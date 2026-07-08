def get_trace_id(headers: dict) -> str | None:
    return headers.get("traceparent") or headers.get("x-trace-id")
