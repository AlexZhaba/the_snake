from typing import override

from model.game_object import Drawer, GameObject, Position

APPLE_COLOR_RGB = (255, 0, 0)


class Apple(GameObject):
    def __init__(self, position: Position, drawer: Drawer) -> None:
        super().__init__(position, APPLE_COLOR_RGB, drawer)

    @override
    def draw(self) -> None:
        self.drawer.rect(position=self.position, size=(1, 1), color=self.body_color)
