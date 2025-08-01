from typing import TYPE_CHECKING
from .entity import Entity

if TYPE_CHECKING:
    from pyglet_dragonbones.skeleton import Skeleton


class SkeletalEntity(Entity):
    skeleton: "Skeleton"

    def move(self, dt: float, move_angle: float):
        self.run_animation("run")
        super().move(dt, move_angle)

    def stand(self):
        """Make the skeletal entity stand."""
        self.run_animation(None)
        super().stand()

    def set_angle(self, angle: float):
        """Set the angle of the skeletal entity."""
        self.skeleton.set_angle(angle)

    @property
    def angle(self):
        return self.skeleton.angle

    def set_target_angle(self, angle: float):
        """Set the target angle of the skeletal entity."""
        self.skeleton.set_target_angle(angle)

    def update_angle_to_target(self, dt: float):
        """Update the angle of the skeletal entity to the target angle."""
        self.skeleton.update_angle_to_target(dt)

    def run_animation(self, animation_name: str | None, starting_frame=0, speed=1):
        """Run an animation on the skeletal entity."""
        self.skeleton.run_animation(animation_name, starting_frame, speed)

    def cleanup(self):
        if hasattr(self, "skeleton"):
            del self.skeleton.batch
            del self.skeleton
