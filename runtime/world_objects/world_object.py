class WorldObject:
    def __init__(self, runtime):
        self.runtime = runtime
        self._position = (0.0, 0.0)

        self._bounding_box: tuple[float, float, float, float] | None = None

    @property
    def bounding_box(self):
        return self._bounding_box

    @bounding_box.setter
    def bounding_box(self, bounding_box: tuple[float, float, float, float]):
        self._bounding_box = bounding_box

    @property
    def position(self):
        """Get the position of the world object."""
        return self._position

    @position.setter
    def position(self, position: tuple[float, float]):
        """Set the position of the world object."""
        self._position = position

    def update(self, dt):
        """Update the world object."""
        pass

    def draw(self, dt):
        """Draw the world object."""
        pass

    @property
    def tile_size(self):
        """Get the size of a tile in the world."""
        return self.runtime.level.map.tile_size

    def check_collision(self, other):
        """Check if this item collides with another object's bounding box."""
        if not self.bounding_box or not other.bounding_box:
            return False

        x1_min, y1_min, x1_max, y1_max = self.bounding_box
        x2_min, y2_min, x2_max, y2_max = other.bounding_box

        return not (
            x1_max < x2_min or x1_min > x2_max or y1_max < y2_min or y1_min > y2_max
        )

    def cleanup(self):
        pass
