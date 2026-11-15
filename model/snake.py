"""Движение и отрисовка змейки"""

from collections import deque
from typing import override

from constants import CELL_SIZE, RIGHT, SNAKE_COLOR_RGB
from model.drawer import BodyColor, Drawer, Position
from model.game_object import GameObject


class Snake(GameObject):
    """Голова лежит в начале очереди"""

    def __init__(
        self,
        position: Position | None = None,
        body_color: BodyColor = SNAKE_COLOR_RGB,
        drawer: Drawer | None = None,
    ) -> None:
        """Создаём змейку, движущуюся вправо"""
        super().__init__(position, body_color, drawer)
        self.positions = deque([self.position])
        self.direction = RIGHT
        self.next_direction = None
        self.last: Position | None = None

    @property
    def length(self) -> int:
        """Длина змейки в клетках"""
        return len(self.positions)

    def get_head_position(self) -> Position:
        """Текущая клетка головы"""
        return self.positions[0]

    def update_direction(self) -> None:
        """Меняем направление следующего хода"""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def get_next_move(self) -> tuple[Position, Position]:
        """Считаем ход с переходом через край поля"""
        width, height = self.drawer.get_grid_size()
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0]) % width,
            (head[1] + self.direction[1]) % height,
        )
        return head, new_head

    def move(self, with_extend: bool = False) -> None:
        """Двигаем голову, при росте оставляем хвост"""
        _, self.position = self.get_next_move()
        self.positions.appendleft(self.position)
        self.last = None if with_extend else self.positions.pop()

    def reset(self, position: Position | None = None) -> None:
        """Возвращаем короткую змейку и очищаем поле"""
        if position is None:
            width, height = self.drawer.get_grid_size()
            position = (width // 2, height // 2)
        self.position = position
        self.positions = deque([position])
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.drawer.fill_all_area()

    @override
    def draw(self) -> None:
        """Стираем хвост и рисуем голову"""
        if self.last is not None:
            self.drawer.clear(self.last, CELL_SIZE)
            self.last = None
        self.draw_cell(self.position)
