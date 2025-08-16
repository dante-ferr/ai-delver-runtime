from typing import cast, Any
from .world_objects import WorldObjectsController, WorldObject
from .world_objects.entities.delver import Delver
from .world_objects.items import Goal
import pymunk
from pytiling import (
    TilemapBorderTracer,
    PymunkTilemapPhysics,
)
from typing import TYPE_CHECKING
from .config import PHYSICS_FPS

if TYPE_CHECKING:
    from level.level import Level


class Runtime:

    def __init__(self, level: Any, render: bool, physics: bool = True):
        self.render = render
        self.level: "Level" = level
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        self.space.iterations = 30

        self.execution_speed = 1.0

        self.physics = physics
        self.physics_dt = 1.0 / PHYSICS_FPS
        self.physics_accumulator = 0.0

        self._setup_wall_physics()

        self.running = False

        self.world_objects_controller = self.world_objects_controller_factory(
            self.space
        )
        self.delver = cast(
            "Delver", self.world_objects_controller.get_world_object("delver")
        )
        self.goal = self.world_objects_controller.get_world_object("goal")

    def update(self, dt):
        self.world_objects_controller.update_world_objects(dt)

        if self.physics:
            self.update_physics(dt)

    def update_physics(self, dt):
        self.physics_accumulator += dt

        while self.physics_accumulator >= self.physics_dt:
            self.space.step(self.physics_dt)
            self.physics_accumulator -= self.physics_dt

    def run(self):
        self.running = True

    def stop(self):
        if not self.running:
            return
        self.running = False

    @property
    def tilemap(self):
        return self.level.map.tilemap

    def _setup_wall_physics(self):
        walls = self.level.map.tilemap.get_layer("walls")
        border_tracer = TilemapBorderTracer(walls)
        PymunkTilemapPhysics(border_tracer, self.space)

    def world_objects_controller_factory(self, space: "pymunk.Space"):
        world_objects_controller = WorldObjectsController()

        def _place_world_object(world_object: "WorldObject", **args):
            world_object_actual_pos = self.level.map.grid_pos_to_actual_pos(
                element.position
            )
            world_object.position = (
                world_object_actual_pos[0] + self.level.map.tile_size[0] / 2,
                world_object_actual_pos[1] + self.level.map.tile_size[1] / 2,
            )
            world_objects_controller.add_world_object(world_object, **args)

        def _delver_factory(element):
            delver = Delver(self, space=space, render=self.render)
            delver.angle = 180

            _place_world_object(delver, unique_identifier="delver")

        def _goal_factory(element):
            goal = Goal(self, element.canvas_object_name, render=self.render)

            _place_world_object(goal, unique_identifier="goal")

        world_objects_factories = {"delver": _delver_factory, "goal": _goal_factory}

        for element in self.level.map.world_objects_map.all_elements:
            world_objects_factories[element.name](element)

        return world_objects_controller
