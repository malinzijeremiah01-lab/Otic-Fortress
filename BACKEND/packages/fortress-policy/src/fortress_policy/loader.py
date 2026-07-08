import yaml
from pathlib import Path
from .models import PolicyDocument

def load_policy(path: str | Path) -> PolicyDocument:
    return PolicyDocument.model_validate(yaml.safe_load(Path(path).read_text()))
