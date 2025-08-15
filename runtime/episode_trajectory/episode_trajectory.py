from typing import TYPE_CHECKING
import json
from dataclasses import dataclass, asdict, field
from .trajectory_saver import TrajectorySaver


if TYPE_CHECKING:
    from .delver_action import DelverAction


@dataclass
class EpisodeTrajectory:

    actions_per_second: int
    victorious: bool = False
    delver_actions: "list[DelverAction]" = field(default_factory=list)

    def add_delver_action(self, action: "DelverAction"):
        """Adds a delver action to the trajectory."""
        self.delver_actions.append(action)

    def to_json(self) -> str:
        """Converts the episode trajectory to a JSON string."""
        return json.dumps(asdict(self))

    def save(self, agent_name: str):
        """Saves the current trajectory to the trajectory directory."""
        TrajectorySaver(agent_name).save_trajectory_json(self.to_json())


class EpisodeTrajectoryFactory:
    @staticmethod
    def from_json(json_string: str) -> "EpisodeTrajectory":
        """Creates an EpisodeTrajectory from a JSON string."""
        return EpisodeTrajectory(**json.loads(json_string))
