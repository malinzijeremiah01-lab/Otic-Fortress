def raw_event_path(tenant_id: str, event_id: str) -> str:
    return f"raw-events/tenant_id={tenant_id}/{event_id}.json"
