from typing import TYPE_CHECKING, Literal, Callable
from .entity import Entity

if TYPE_CHECKING:
    from pyglet_dragonbones.skeleton import Skeleton


class SkeletalEntity(Entity):

    def __init__(self, runtime, body, skeleton: "Skeleton"):
        super().__init__(runtime, body)
        self.skeleton = skeleton

    def move(self, dt, move_angle: float):
        self.run_animation("run")
        super().move(dt, move_angle)

        if move_angle > 270 or move_angle < 90:
            self.scale = (1, 1)
        elif move_angle > 90 and move_angle < 270:
            self.scale = (-1, 1)

    def stand(self):
        """Make the skeletal entity stand."""
        self.run_animation("idle")
        super().stand()

    @property
    def angle(self):
        return self.skeleton.angle

    @angle.setter
    def angle(self, angle: float):
        self.skeleton.angle = angle

    @property
    def scale(self):
        return self.skeleton.scale

    @scale.setter
    def scale(self, scale: tuple[float, float]):
        self.skeleton.scale = scale

    @property
    def target_angle(self) -> float | None:
        return self.skeleton.target_angle

    @target_angle.setter
    def target_angle(self, angle: float):
        """Set the target angle of the skeletal entity."""
        self.skeleton.target_angle = angle

    def run_animation(
        self,
        animation_name: str | None,
        starting_frame=0,
        speed=1,
        on_end: Literal["_loop"] | Callable = "_loop",
    ):
        """Run an animation on the skeletal entity."""
        self.skeleton.run_animation(animation_name, starting_frame, speed, on_end)

    def cleanup(self):
        if hasattr(self, "skeleton"):
            del self.skeleton.batch
            del self.skeleton
