from ...utils import angle_to_vector
import math
from pymunk import Vec2d
from typing import TYPE_CHECKING
from ..world_object import WorldObject

if TYPE_CHECKING:
    from .entity_body import EntityBody


class Entity(WorldObject):
    move_speed = 200

    def __init__(self, runtime, body: "EntityBody"):
        super().__init__(runtime)
        self.body = body

    @property
    def shape(self):
        return next(iter(self.body.shapes))

    def move(self, dt: float, move_angle: float):
        """Make the entity move."""
        self.set_target_angle(-move_angle - 90)
        self.update_angle_to_target(dt)

        run_vector = angle_to_vector(move_angle)
        run_velocity: list[float] = [
            run_vector[0] * self.move_speed,
            run_vector[1] * self.move_speed,
        ]

        magnitude = math.sqrt(run_velocity[0] ** 2 + run_velocity[1] ** 2)
        if magnitude > self.move_speed:
            run_velocity[0] *= self.move_speed / magnitude
            run_velocity[1] *= self.move_speed / magnitude

        force = Vec2d(
            self.body.mass * run_velocity[0] / dt,
            self.body.mass * run_velocity[1] / dt,
        )
        self.body.apply_force_at_local_point(force)

    @property
    def position(self):
        """Get the position of the entity."""
        return self.body.position.x, self.body.position.y

    @position.setter
    def position(self, position: tuple[float, float]):
        """Set the position of the entity by changing the position of its body."""
        self.body.position = Vec2d(position[0], position[1])

    def stand(self):
        """Make the entity stand."""
        self.body.velocity = Vec2d(0, 0)

    def set_target_angle(self, angle: float):
        """Set the target angle of the entity."""
        pass

    def update_angle_to_target(self, dt: float):
        """Update the angle of the entity to the target angle."""
        pass

    def update(self, dt):
        """Update the entity."""
        self.bounding_box = (
            self.body.position.x - self.shape.radius,
            self.body.position.y - self.shape.radius,
            self.body.position.x + self.shape.radius,
            self.body.position.y + self.shape.radius,
        )

        super().update(dt)
