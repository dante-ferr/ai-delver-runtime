from ..entity_body import EntityBody
import pymunk


class DelverBody(EntityBody):
    MOVE_FORCE = 2200.0
    LINEAR_DAMPING = 15.0
    BRAKING_FORCE = 900.0
    JUMP_IMPULSE = 350.0

    COLLISION_MASK_SIZE = (16.0, 38.0)
    MASS = 1.0

    JUMP_TOLERANCE_TIMER_MAX = 0.1

    def __init__(self):
        width, height = self.COLLISION_MASK_SIZE

        left = -width / 2
        right = width / 2
        bottom = 0
        top = height

        vertices = [(left, bottom), (right, bottom), (right, top), (left, top)]

        center_of_gravity = (0, bottom)
        super().__init__(self.MASS, float("inf"))

        # The shape's vertices are defined relative to the body's origin.
        self.shape = pymunk.Poly(
            self,
            vertices,
            transform=pymunk.Transform(
                tx=center_of_gravity[0], ty=center_of_gravity[1]
            ),
        )
        self.shape.collision_type = 1
        self.jump_tolerance_timer = 0
        self.jumped = False

    def jump(self):
        if self.is_on_ground or self.jump_tolerance_timer > 0:

            def check_normal(arbiter: pymunk.Arbiter):
                if self.shape == arbiter.shapes[0]:
                    normal = arbiter.contact_point_set.normal
                else:
                    normal = -arbiter.contact_point_set.normal

                print(normal)

            self.each_arbiter(check_normal)

            self.jumped = True
            impulse = (0, self.JUMP_IMPULSE)
            self.apply_impulse_at_local_point(impulse, (0, 0))
            self.jump_tolerance_timer = 0

    def update(self, dt):
        super().update(dt)

        if self.is_on_ground and not self.jumped:
            self.jump_tolerance_timer = self.JUMP_TOLERANCE_TIMER_MAX
        else:
            self.jump_tolerance_timer = max(0, self.jump_tolerance_timer - dt)

        self.jumped = False
