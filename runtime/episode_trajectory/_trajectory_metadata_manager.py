import logging
import json
from ._get_trajectory_dir import get_trajectory_dir
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class TrajectoryMetadataManager:
    METADATA_FILE = "metadata.json"

    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    def write_metadata(self, metadata: dict):
        """Writes the metadata to the trajectory directory."""
        metadata_path = self.trajectory_dir / self.METADATA_FILE
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)

    def read_metadata(self) -> dict:
        """Reads the metadata file from the trajectory directory."""
        metadata_path = self.trajectory_dir / self.METADATA_FILE
        if not metadata_path.exists():
            return {"trajectory_count": 0}
        with open(metadata_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                logging.warning(f"Could not decode {metadata_path}, resetting.")
                return {"trajectory_count": 0}

    @property
    def trajectory_dir(self) -> "Path":
        return get_trajectory_dir(self.agent_name)
