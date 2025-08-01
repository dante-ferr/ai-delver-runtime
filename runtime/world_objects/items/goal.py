from .item import Item


class Goal(Item):
    def __init__(self, runtime, variation: str, render):
        super().__init__(
            runtime, f"assets/img/representations/goal/{variation}.png", render=render
        )
