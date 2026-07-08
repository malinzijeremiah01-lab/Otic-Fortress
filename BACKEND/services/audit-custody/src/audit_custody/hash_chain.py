import hashlib
import json

def hash_record(record: dict, previous_hash: str | None = None) -> str:
    payload = {"previous_hash": previous_hash, "record": record}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
