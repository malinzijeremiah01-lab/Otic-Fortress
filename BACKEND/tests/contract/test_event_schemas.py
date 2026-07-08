from pathlib import Path
import json


def test_event_schemas_are_valid_json():
    for path in Path("schemas/events").glob("*.json"):
        json.loads(path.read_text())
