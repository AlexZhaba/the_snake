import collections
from collections import deque
from typing import override

from model.game_object import Drawer, GameObject, Position

SNAKE_COLOR_RGB = (0, 255, 0)
SNAKE_BLOCK_SIZE_IN_GRID = (1, 1)


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


type Direction = tuple[int, int]


class Snake(GameObject):
    """Змейка. Голова лежит в начале очереди."""

    direction: Direction
    positions: collections.deque[Position]
    old_positions: list[Position]

    def __init__(
        self,
        position: list[Position] | None = None,
        drawer: Drawer | None = None,
    ) -> None:
        super().__init__(position, SNAKE_COLOR_RGB, drawer)
        self.direction = RIGHT
        self.old_positions = []

    @property
    def length(self) -> int:
        """Длина змейки по количеству клеток."""
        return len(self.positions)

    def get_head_position(self) -> Position:
        """Клетка, в которой сейчас голова."""
        return self.positions[0]

    def update_direction(self, new_direction: tuple[int, int]) -> None:
        """Меняем направление для следующего хода."""
        self.direction = new_direction

    def get_next_move(self) -> tuple[Position, Position]:
        """Считаем следующий ход с переходом через край поля."""
        grid_size_x, grid_size_y = self.drawer.get_grid_size()
        head = self.get_head_position()

        # А тут я забил в codex вопрос "как учесть отрицательные числа"
        # И узнал что -1 % 10 -> 9, забавно
        new_head_x, new_head_y = (
            (head[0] + self.direction[0]) % grid_size_x,
            (head[1] + self.direction[1]) % grid_size_y,
        )
        return (head, (new_head_x, new_head_y))

    def move(self, with_extend: bool = False) -> None:
        """Двигаем змейку. При росте хвост оставляем."""
        _, new_head = self.get_next_move()
        self.positions.appendleft(new_head)

        if not with_extend:
            self.old_positions.append(self.positions.pop())

    def reset(self, new_positions: list[Position]) -> None:
        """Сбрасываем змейку, старые клетки потом сотрем."""
        self.old_positions = list(self.positions.copy())
        self.positions = deque(new_positions)

    @override
    def draw(self) -> None:
        """Сначала стираем старые клетки, потом рисуем змейку."""
        for old_position in self.old_positions:
            self.drawer.clear(old_position, SNAKE_BLOCK_SIZE_IN_GRID)
        self.old_positions = []

        for position in self.positions:
            self.drawer.rect(
                position, SNAKE_BLOCK_SIZE_IN_GRID, self.body_color
            )
