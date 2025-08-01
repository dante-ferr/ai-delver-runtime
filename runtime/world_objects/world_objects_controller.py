from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .entities.entity import WorldObject


class WorldObjectsController:
    def __init__(self):
        self.world_objects: set["WorldObject"] = set()
        self.world_object_groups: dict[str, set["WorldObject"]] = {}

    def add_world_object(
        self,
        world_object: "WorldObject",
        group_name: str | None = None,
        unique_identifier: str | None = None,
    ):
        self.world_objects.add(world_object)

        if group_name is not None:
            if group_name not in self.world_object_groups.keys():
                self.world_object_groups[group_name] = set()
            self.world_object_groups[group_name].add(world_object)

        if unique_identifier is not None:
            setattr(self, unique_identifier, world_object)

    def get_world_object(self, name: str) -> "WorldObject":
        return getattr(self, name)

    def update_world_objects(self, dt: float):
        for world_object in self.world_objects:
            world_object.update(dt)

    def draw_world_objects(self, dt: float):
        for world_object in self.world_objects:
            world_object.draw(dt)
