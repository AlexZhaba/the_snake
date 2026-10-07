from random import randint
from typing import Self, override

from model.game_object import Drawer, GameObject, Position

APPLE_COLOR_RGB = (255, 0, 0)


class Apple(GameObject):
    """Яблоко, занимает одну клетку."""

    def __init__(
        self, position: Position | None = None, drawer: Drawer | None = None
    ) -> None:
        positions = [position] if position is not None else None
        super().__init__(positions, APPLE_COLOR_RGB, drawer)
        if position is None:
            self.randomize_position()

    def randomize_position(self) -> None:
        """Ставим яблоко в случайную клетку поля."""
        grid_size_x, grid_size_y = self.drawer.get_grid_size()
        self.position = (
            randint(0, grid_size_x - 1),
            randint(0, grid_size_y - 1),
        )

    @override
    def draw(self) -> None:
        """Рисуем яблоко."""
        self.drawer.rect(
            position=self.positions[0], size=(1, 1), color=self.body_color
        )

    @classmethod
    def create_at_random_place(cls, drawer: Drawer) -> Self:
        """Создаём яблоко в случайном месте."""
        return cls(drawer=drawer)
