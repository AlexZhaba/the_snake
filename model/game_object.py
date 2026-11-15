"""Общий класс объектов игры"""

from constants import CELL_SIZE, SNAKE_COLOR_RGB
from model.drawer import BodyColor, Drawer, Position
from model.pygame_drawer import get_default_drawer


class GameObject:
    """Позиция, цвет и отрисовщик объекта"""

    def __init__(
        self,
        position: Position | None = None,
        body_color: BodyColor = SNAKE_COLOR_RGB,
        drawer: Drawer | None = None,
    ) -> None:
        """По умолчанию ставим объект в центр поля"""
        self.drawer = drawer if drawer is not None else get_default_drawer()
        if position is None:
            width, height = self.drawer.get_grid_size()
            position = (width // 2, height // 2)
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Отрисовку определяет наследник"""
        raise NotImplementedError(type(self).__name__)

    def draw_cell(self, position: Position) -> None:
        """Рисуем одну клетку"""
        self.drawer.rect(position, CELL_SIZE, self.body_color)
