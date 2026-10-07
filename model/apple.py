from random import randint
from typing import Self, override

from model.game_object import Drawer, GameObject, Position

APPLE_COLOR_RGB = (255, 0, 0)


class Apple(GameObject):
    def __init__(self, position: Position, drawer: Drawer) -> None:
        super().__init__([position], APPLE_COLOR_RGB, drawer)

    @override
    def draw(self) -> None:
        self.drawer.rect(position=self.positions[0], size=(1, 1), color=self.body_color)

    @classmethod
    def create_at_random_place(cls, drawer: Drawer) -> Self:
        grid_size_x, grid_size_y = drawer.get_grid_size()
        return cls((randint(0, grid_size_x - 1), randint(0, grid_size_y - 1)), drawer)
