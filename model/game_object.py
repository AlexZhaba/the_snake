from abc import ABC, abstractmethod
from collections import deque
from typing import Protocol

type Position = tuple[int, int]
type BodyColor = tuple[int, int, int]


class Drawer(Protocol):
    def rect(
        self, position: Position, size: tuple[int, int], color: BodyColor
    ) -> None: ...
    def get_grid_size(self) -> tuple[int, int]: ...
    def clear(self, position: Position, size: tuple[int, int]): ...
    def fill_all_area(self) -> None: ...
    def update_area(self) -> None: ...


class GameObject(ABC):
    positions: deque[Position]
    body_color: BodyColor
    drawer: Drawer

    def __init__(
        self, positions: list[Position], body_color: BodyColor, drawer: Drawer
    ) -> None:
        # Поскольку надо удалять хвост и добавлять голову, хочется это делать за O(1)
        # А писать собственную эффективную очередь не хотелось
        self.positions = deque(positions)
        self.body_color = body_color
        self.drawer = drawer

    @abstractmethod
    def draw(self) -> None:
        pass

    def get_positions(self):
        return self.positions

    def get_intersection_with(self, positions: list[tuple[int, int]]):
        intersection = set(self.get_positions()) & set(positions)

        return intersection
