import pymunk
from typing import Literal
from .entity import EntityState
import math
from pymunk import Vec2d

class EntityBody(pymunk.Body):
    # Default physics parameters for this body type.
    MOVE_FORCE = 3200.0
    LINEAR_DAMPING = 20.0
    BRAKING_FORCE = 2000.0
    MIN_VELOCITY_TO_BRAKE = 10.0
    KNOCKBACK_FORCE_THRESHOLD = 100000.0
    TUMBLING_FORCE_THRESHOLD = 250000.0

    def __init__(self, mass: float = 0, moment: float = 0):
        """
        A Body object that holds the physics representation of an entity.
        """
        super().__init__(mass, moment)

        # Assign constants to instance variables for potential per-instance modification.
        self.move_force = EntityBody.MOVE_FORCE
        self.braking_force = EntityBody.BRAKING_FORCE
        self.min_velocity_to_brake = EntityBody.MIN_VELOCITY_TO_BRAKE

    def setup_collision_handlers(self):
        if not self.space:
            raise ValueError("Space not set for the entity's body.")
        collision_handler = self.space.add_collision_handler(1, 2)
        collision_handler.pre_solve = self._on_collision_pre_solve

    def _on_collision_pre_solve(self, arbiter, space, data):
        if self.entity.state != EntityState.NORMAL:
            self.entity.return_to_normal_state()
        return True

    def apply_damping(self):
        damping_force = -self.velocity * self.LINEAR_DAMPING
        self.apply_force_at_local_point(damping_force)

    def move(self, move_angle: float):
        move_direction = Vec2d(1, 0).rotated(math.radians(move_angle))
        force_vector = move_direction * self.move_force
        self.apply_force_at_local_point(force_vector)

    def brake(self):
        if self.velocity.length > self.min_velocity_to_brake:
            braking_vector = -self.velocity.normalized() * self.braking_force
            self.apply_force_at_local_point(braking_vector)
        else:
            self.velocity = Vec2d(0, 0)
            self.angular_velocity = 0

    def receive_impact(self, impulse_vector: Vec2d):
        self.apply_impulse_at_local_point(impulse_vector)
