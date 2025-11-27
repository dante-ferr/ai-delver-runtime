from ..entity_body import EntityBody
import pymunk


class DelverBody(EntityBody):
    MOVE_FORCE = 700.0
    LINEAR_DAMPING = 4.0
    BRAKING_FORCE = 700.0
    JUMP_IMPULSE = 350.0

    COLLISION_MASK_SIZE = (16.0, 32.0)
    MASS = 1.0

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

    def jump(self):
        impulse = (0, self.JUMP_IMPULSE)
        print(impulse)
        self.apply_impulse_at_local_point(impulse, (0, 0))
