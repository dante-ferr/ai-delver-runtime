import pyglet
from pyglet_dragonbones.skeleton import Skeleton
from .delver_body import DelverBody
import pymunk
from ..skeletal_entity import SkeletalEntity
from runtime.config import ASSETS_PATH


class Delver(SkeletalEntity):
    run_angle = 0.0

    def __init__(self, runtime, space: pymunk.Space, render=True):
        mass = 1
        radius = 10
        body = DelverBody(mass=mass, moment=pymunk.moment_for_circle(mass, 0, radius))

        shape = pymunk.Circle(body, radius)
        shape.collision_type = 1
        space.add(body, shape)

        body.setup_collision_handlers()

        super().__init__(runtime, body, self._skeleton_factory(render))

    def _skeleton_factory(self, render):
        if render == True:
            delver_groups = {
                "feather": pyglet.graphics.Group(6),
                "head": pyglet.graphics.Group(5),
                "front_hand": pyglet.graphics.Group(4),
                "torso": pyglet.graphics.Group(3),
                "back_hand": pyglet.graphics.Group(2),
                "front_foot": pyglet.graphics.Group(1),
                "back_foot": pyglet.graphics.Group(0),
            }
        else:
            delver_groups = None

        skeleton = Skeleton(
            str(ASSETS_PATH / "img/sprites/delver"), groups=delver_groups, render=render
        )
        for bone in skeleton.bones.values():
            bone.transform.smoothing_enabled["scale"] = False

        return skeleton

    def draw(self, dt):
        self.skeleton.draw(dt)
        super().draw(dt)

    def update(self, dt):
        self.skeleton.position = (self.body.position.x, self.body.position.y)
        self.skeleton.update(dt)

        super().update(dt)
