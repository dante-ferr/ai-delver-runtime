from enum import Enum, auto
from typing import TYPE_CHECKING, Literal, Callable
from .entity import Entity

if TYPE_CHECKING:
    from pyglet_dragonbones.skeleton import Skeleton


class LocomotionState(Enum):
    IDLE = auto()
    RUN = auto()
    GO_UP = auto()
    FALL = auto()
    LAND = auto()


class SkeletalEntity(Entity):
    LAND_ANIMATION_REQUIRED_FALLING_SPEED = -250.0

    def __init__(self, runtime, body, skeleton: "Skeleton"):
        super().__init__(runtime, body)
        self.skeleton = skeleton
        self.locomotion_state = LocomotionState.IDLE
        self.previous_on_air_velocity = (0, 0)

    def move(self, dt, move_angle: float):
        super().move(dt, move_angle)

        if move_angle > 270 or move_angle < 90:
            self.scale = (1, 1)
        elif move_angle > 90 and move_angle < 270:
            self.scale = (-1, 1)

    def stand(self):
        """Make the skeletal entity stand."""
        super().stand()

    def update(self, dt):
        # Capture intention before super().update() resets it
        is_moving = self.is_moving_intentionally

        super().update(dt)

        self._update_locomotion_state(is_moving)
        if not self.is_on_ground:
            # Only update if velocity is significant. This prevents overwriting the
            # falling velocity with 0 on the specific frame where the physics has stopped
            # the body (collision) but the raycast (is_on_ground) hasn't updated yet.
            if abs(self.velocity.y) > 1.0:
                self.previous_on_air_velocity = (self.velocity.x, self.velocity.y)

    def _update_locomotion_state(self, is_moving: bool):
        new_state = self.locomotion_state

        if self.is_on_ground:
            if self.locomotion_state in (LocomotionState.GO_UP, LocomotionState.FALL):
                print(self.previous_on_air_velocity[1])
                if (
                    self.previous_on_air_velocity[1]
                    <= self.LAND_ANIMATION_REQUIRED_FALLING_SPEED
                ):
                    new_state = LocomotionState.LAND
                else:
                    new_state = (
                        LocomotionState.RUN if is_moving else LocomotionState.IDLE
                    )
            elif self.locomotion_state == LocomotionState.LAND:
                # if is_moving:
                #    new_state = LocomotionState.RUN
                pass
            else:
                new_state = LocomotionState.RUN if is_moving else LocomotionState.IDLE
        else:
            new_state = (
                LocomotionState.GO_UP if self.velocity.y > 0 else LocomotionState.FALL
            )

        if new_state != self.locomotion_state:
            self.locomotion_state = new_state
            self._play_locomotion_animation()

    def _play_locomotion_animation(self):
        if self.locomotion_state == LocomotionState.IDLE:
            self.run_animation("idle")
        elif self.locomotion_state == LocomotionState.RUN:
            self.run_animation("run")
        elif self.locomotion_state == LocomotionState.GO_UP:
            self.run_animation("go_up")
        elif self.locomotion_state == LocomotionState.FALL:
            self.run_animation("fall")
        elif self.locomotion_state == LocomotionState.LAND:
            self.run_animation("land", on_end=self._on_land_finish)

    def _on_land_finish(self):
        if self.locomotion_state == LocomotionState.LAND:
            self.locomotion_state = LocomotionState.IDLE
            self._play_locomotion_animation()

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
