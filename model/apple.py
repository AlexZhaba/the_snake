"""Яблоко на игровом поле"""

from collections.abc import Collection
from random import choice
from typing import override

from constants import APPLE_COLOR_RGB
from model.drawer import BodyColor, Drawer, Position
from model.game_object import GameObject


class Apple(GameObject):
    """Яблоко занимает одну свободную клетку"""

    def __init__(
        self,
        occupied_positions: Collection[Position] = (),
        body_color: BodyColor = APPLE_COLOR_RGB,
        drawer: Drawer | None = None,
    ) -> None:
        """Выбираем место вне змейки"""
        super().__init__(body_color=body_color, drawer=drawer)
        self.randomize_position(occupied_positions)

    def randomize_position(
        self, occupied_positions: Collection[Position] = ()
    ) -> None:
        """Переносим яблоко на свободную клетку"""
        width, height = self.drawer.get_grid_size()
        occupied = set(occupied_positions)
        free_positions = [
            (x, y)
            for x in range(width)
            for y in range(height)
            if (x, y) not in occupied
        ]
        if not free_positions:
            raise ValueError('На поле нет свободных клеток')
        self.position = choice(free_positions)

    @override
    def draw(self) -> None:
        """Рисуем яблоко"""
        self.draw_cell(self.position)
