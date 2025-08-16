from enum import Enum, auto
from typing import TYPE_CHECKING
from ..world_object import WorldObject
from pymunk import Vec2d

if TYPE_CHECKING:
    from .entity_body import EntityBody


class EntityState(Enum):
    """Defines the possible states of the entity."""

    NORMAL = auto()
    KNOCKBACK = auto()
    TUMBLING = auto()


class Entity(WorldObject):

    def __init__(self, runtime, body: "EntityBody"):
        super().__init__(runtime)
        self.body = body
        self.body.entity = self
        self.state = EntityState.NORMAL
        self.is_moving_intentionally = False

    @property
    def shape(self):
        return next(iter(self.body.shapes))

    def move(self, dt, move_angle: float):
        if self.state != EntityState.NORMAL:
            return
        self.set_target_angle(-move_angle - 90)
        self.update_angle_to_target(dt)
        self.is_moving_intentionally = True
        self.body.move(move_angle)

    def brake(self):
        if self.state != EntityState.NORMAL:
            return
        self.body.brake()

    def receive_impact(self, impulse_vector: Vec2d):
        impulse_magnitude = impulse_vector.length
        if impulse_magnitude >= self.body.TUMBLING_FORCE_THRESHOLD:
            self.state = EntityState.TUMBLING
            print("STATE CHANGE: TUMBLING")
        elif impulse_magnitude >= self.body.KNOCKBACK_FORCE_THRESHOLD:
            self.state = EntityState.KNOCKBACK
            print("STATE CHANGE: KNOCKBACK")
        self.body.receive_impact(impulse_vector)

    def return_to_normal_state(self):
        if self.state != EntityState.NORMAL:
            print("STATE CHANGE: NORMAL")
            self.state = EntityState.NORMAL

    def stand(self):
        self.brake()

    def update(self, dt):
        if self.state == EntityState.NORMAL:
            if self.is_moving_intentionally:
                self.body.apply_damping()
            else:
                self.stand()
        self.is_moving_intentionally = False

    @property
    def position(self):
        return self.body.position.x, self.body.position.y

    @position.setter
    def position(self, position: tuple[float, float]):
        self._conditionally_set_spawn_based_id(position)
        self.body.position = Vec2d(position[0], position[1])

    @property
    def angle(self):
        return self.body.angle

    @angle.setter
    def angle(self, angle: float):
        self.body.angle = angle

    def set_target_angle(self, angle: float):
        pass

    def update_angle_to_target(self, dt: float):
        pass
