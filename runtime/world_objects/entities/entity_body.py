import pymunk
from .entity import EntityState
import math
from pymunk import Vec2d

class EntityBody(pymunk.Body):
    MOVE_FORCE: float
    LINEAR_DAMPING: float
    BRAKING_FORCE: float
    MIN_VELOCITY_TO_BRAKE = 10.0
    KNOCKBACK_FORCE_THRESHOLD = 100000.0
    TUMBLING_FORCE_THRESHOLD = 250000.0
    GROUND_THRESHOLD = 0.7

    def __init__(self, mass: float = 0, moment: float = 0):
        """
        A Body object that holds the physics representation of an entity.
        """
        super().__init__(mass, moment)

        # Assign constants to instance variables for per-instance modification.
        self.move_force = self.MOVE_FORCE
        self.braking_force = self.BRAKING_FORCE
        self.min_velocity_to_brake = self.MIN_VELOCITY_TO_BRAKE

    def setup_collision_handlers(self):
        if not self.space:
            raise ValueError("Space not set for the entity's body.")
        collision_handler = self.space.add_collision_handler(1, 2)
        collision_handler.pre_solve = self._on_collision_pre_solve

    def _on_collision_pre_solve(self, arbiter, space, data):
        if self.entity.state != EntityState.NORMAL:
            self.entity.return_to_normal_state()
        return True

    def move(self, move_angle: float):
        move_direction = Vec2d(1, 0).rotated(math.radians(move_angle))
        force_vector = move_direction * self.move_force

        # Apply braking force to change direction faster when moving opposite to current velocity.
        if self.velocity.x * move_direction.x < 0:
            braking_direction_x = (
                -self.velocity.x / abs(self.velocity.x) if self.velocity.x != 0 else 0
            )
            braking_force_vector = Vec2d(braking_direction_x * self.braking_force, 0)
            self.apply_force_at_local_point(braking_force_vector)

        self.apply_force_at_local_point(force_vector)

    def apply_damping(self):
        """Apply damping only to the horizontal component of velocity."""
        horizontal_velocity = Vec2d(self.velocity.x, 0)
        damping_force = -horizontal_velocity * self.LINEAR_DAMPING
        self.apply_force_at_local_point(damping_force)

    def brake(self):
        """Brakes horizontal movement while preserving vertical velocity."""
        if abs(self.velocity.x) > self.min_velocity_to_brake:
            braking_direction_x = (
                -self.velocity.x / abs(self.velocity.x) if self.velocity.x != 0 else 0
            )
            braking_vector_x = Vec2d(braking_direction_x * self.braking_force, 0)
            self.apply_force_at_local_point(braking_vector_x)
        else:
            # If horizontal velocity is very low, set it to zero.
            self.velocity = Vec2d(0, self.velocity.y)
            self.angular_velocity = 0

    def receive_impact(self, impulse_vector: Vec2d):
        self.apply_impulse_at_local_point(impulse_vector)

    def update(self, dt):
        pass

    @property
    def is_on_ground(self) -> bool:
        """
        Checks if the entity is on the ground using a segment query (raycast) downwards.
        """
        if self.space == None:
            return False

        radius = 0
        if hasattr(self.shape, "radius"):
            radius = self.shape.radius

        start = self.position + Vec2d(0, -1)
        # Raycast down by radius + a small buffer.
        cast_distance = Vec2d(0, radius + 5.0)
        end = self.position + cast_distance

        query = self.space.segment_query_first(
            start, end, 1.0, pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS())
        )

        # Validate the hit, ensuring it's not the entity's own shape.
        if query and query.shape != self.shape:
            # Check the normal of the hit surface to ensure it's not a steep slope.
            if query.normal.y < -self.GROUND_THRESHOLD:
                return True

        return False
