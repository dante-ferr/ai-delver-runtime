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

        # Assign constants to instance variables for potential per-instance modification.
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

        # Check if trying to move in the opposite direction of current velocity
        if self.velocity.x * move_direction.x < 0:
            # Apply braking force to change direction faster
            braking_direction_x = (
                -self.velocity.x / abs(self.velocity.x) if self.velocity.x != 0 else 0
            )
            braking_force_vector = Vec2d(braking_direction_x * self.braking_force, 0)
            self.apply_force_at_local_point(braking_force_vector)

        self.apply_force_at_local_point(force_vector)

    def apply_damping(self):
        # Apply damping only to the horizontal component of velocity
        horizontal_velocity = Vec2d(self.velocity.x, 0)
        damping_force = -horizontal_velocity * self.LINEAR_DAMPING
        self.apply_force_at_local_point(damping_force)

    def brake(self):
        # Only brake horizontal movement, preserve vertical velocity
        if abs(self.velocity.x) > self.min_velocity_to_brake:
            # Calculate braking force for horizontal component
            # Ensure braking_direction_x is 1 or -1, or 0 if velocity.x is 0
            braking_direction_x = (
                -self.velocity.x / abs(self.velocity.x) if self.velocity.x != 0 else 0
            )
            braking_vector_x = Vec2d(braking_direction_x * self.braking_force, 0)
            self.apply_force_at_local_point(braking_vector_x)
        else:
            # If horizontal velocity is very low, set it to zero, preserve vertical velocity
            self.velocity = Vec2d(0, self.velocity.y)
            self.angular_velocity = 0

    def receive_impact(self, impulse_vector: Vec2d):
        self.apply_impulse_at_local_point(impulse_vector)

    def update(self, dt):
        pass

    @property
    def is_on_ground(self) -> bool:
        """
        Checks if the body is currently on a walkable surface by inspecting
        the collision normals of all contact points.
        """
        is_grounded = False

        def check_normal(arbiter: pymunk.Arbiter):
            nonlocal is_grounded
            if is_grounded:
                return

            if self.shape == arbiter.shapes[0]:
                normal = arbiter.contact_point_set.normal
            else:
                normal = -arbiter.contact_point_set.normal

            # Check if the normal is pointing sufficiently "up" (negative Y)
            if normal.y < -self.GROUND_THRESHOLD:
                is_grounded = True

        # Call each_arbiter with ONLY the callback function.
        self.each_arbiter(check_normal)

        return is_grounded
