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
    length: int = 1
    positions: deque[Position]
    direction: Direction
    old_positions: list[Position]

    def __init__(self, position: Position, drawer: Drawer) -> None:
        super().__init__(position, SNAKE_COLOR_RGB, drawer)
        # Поскольку надо удалять хвост и добавлять голову, хочется это делать за O(1)
        # А писать собственную эффективную очередь не хотелось
        self.positions = deque([position])
        self.direction = RIGHT
        self.old_positions = []

    def get_head_position(self) -> Position:
        return self.positions[0]

    def move(self) -> None:
        grid_size_y, grid_size_x = self.drawer.get_grid_size()
        head = self.positions.pop()

        # А тут я забил в codex вопрос "как учесть отрицательные числа"
        # И узнал что -1 % 10 -> 9, забавно
        new_head_x, new_head_y = (
            (head[0] + self.direction[0]) % grid_size_x,
            (head[1] + self.direction[1]) % grid_size_y,
        )

        self.positions.appendleft((new_head_x, new_head_y))
        self.old_positions.append(head)

    @override
    def draw(self) -> None:
        for position in self.positions:
            self.drawer.rect(position, SNAKE_BLOCK_SIZE_IN_GRID, self.body_color)

        for old_position in self.old_positions:
            self.drawer.clear(old_position, SNAKE_BLOCK_SIZE_IN_GRID)
