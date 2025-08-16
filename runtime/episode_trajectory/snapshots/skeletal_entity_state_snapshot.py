from dataclasses import dataclass, field
from .entity_state_snapshot import (
    EntityStateSnapshot,
    EntityStateSnapshotFactory,
)
from runtime.world_objects.entities.skeletal_entity import SkeletalEntity
from typing import cast, TYPE_CHECKING, Any


if TYPE_CHECKING:
    from runtime.world_objects.entities.entity import Entity


@dataclass
class SkeletalEntityStateSnapshot(EntityStateSnapshot):
    """
    Captures the complete state of a single skeletal entity at a moment in time.
    This is designed to be easily serialized to JSON.
    """

    animation_name: str | None = field(default=None)

    entity_type: str = field(default="SkeletalEntity")

    def apply_to_entity(self, entity: "Entity"):
        super().apply_to_entity(entity)

        entity = cast("SkeletalEntity", entity)
        entity.run_animation(self.animation_name)


class SkeletalEntityStateSnapshotFactory(EntityStateSnapshotFactory):
    def _get_state_snapshot_args(self, entity: "Entity"):
        entity = cast("SkeletalEntity", entity)

        return {
            **super()._get_state_snapshot_args(entity),
            "animation_name": entity.skeleton.current_animation_name,
        }

    def create_state_snapshot_from_entity(
        self, entity: "Entity"
    ) -> SkeletalEntityStateSnapshot:
        entity = cast("SkeletalEntity", entity)

        return SkeletalEntityStateSnapshot(**self._get_state_snapshot_args(entity))

    def create_state_snapshot_from_json(
        self, json: dict[str, Any]
    ) -> SkeletalEntityStateSnapshot:
        return SkeletalEntityStateSnapshot(**json)
