from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from .delver_action import DelverAction


class EpisodeTrajectory:
    def __init__(self):
        self.delver_actions: "list[DelverAction]" = []

    def add_delver_action(self, action: "DelverAction"):
        self.delver_actions.append(action)

    def to_json(self) -> str:
        """Converts the episode trajectory to a JSON string."""
        return json.dumps({"delver_actions": self.delver_actions})


class EpisodeTrajectoryFactory:
    @staticmethod
    def from_json(json_string: str) -> "EpisodeTrajectory":
        """Creates an EpisodeTrajectory from a JSON string."""
        data = json.loads(json_string)
        trajectory = EpisodeTrajectory()
        # Use .get() for safety in case the key is missing
        trajectory.delver_actions = data.get("delver_actions", [])
        return trajectory
