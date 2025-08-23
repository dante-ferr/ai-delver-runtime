from ._trajectory_metadata_manager import TrajectoryMetadataManager
from ._get_trajectory_dir import get_trajectory_dir
import json
import logging
from typing import TYPE_CHECKING, Optional
import asyncio

if TYPE_CHECKING:
    from pathlib import Path
    from .episode_trajectory import EpisodeTrajectory


class TrajectoryStatsCalculator:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name

        self.metadata_manager = TrajectoryMetadataManager(agent_name)

    async def get_stats(self):
        from .episode_trajectory import EpisodeTrajectoryFactory
        import aiofiles

        stats = {
            "amount": self.get_amount_of_trajectories(),
            "victories": 0,
        }

        async def read_and_parse_trajectory(
            file_path: "Path",
        ) -> Optional["EpisodeTrajectory"]:
            try:
                async with aiofiles.open(file_path, mode="r") as f:
                    content = await f.read()
                    return EpisodeTrajectoryFactory.from_json(content)
            except (json.JSONDecodeError, IOError) as e:
                logging.warning(f"Could not read or parse trajectory {file_path}: {e}")
                return None

        tasks = []
        for trajectory_file_path in self.trajectory_dir.glob("trajectory_*.json"):
            task = asyncio.create_task(read_and_parse_trajectory(trajectory_file_path))
            tasks.append(task)

        for future in asyncio.as_completed(tasks):
            trajectory = await future
            if trajectory and trajectory.victorious:
                stats["victories"] += 1

        return stats

    def get_amount_of_trajectories(self) -> int:
        metadata = self.metadata_manager.read_metadata()
        amount = metadata.get("trajectory_count", 0)
        return amount

    @property
    def trajectory_dir(self) -> "Path":
        return get_trajectory_dir(self.agent_name)
