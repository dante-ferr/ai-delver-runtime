from .runtime import Runtime
import json
from pathlib import Path

with open(Path(__file__).parent / "config.json", "r") as file:
    config = json.load(file)

__all__ = ["Runtime", "config"]
