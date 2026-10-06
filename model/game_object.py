from abc import ABC, abstractmethod
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
    position: Position
    body_color: BodyColor
    drawer: Drawer

    def __init__(
        self, position: Position, body_color: BodyColor, drawer: Drawer
    ) -> None:
        self.position = position
        self.body_color = body_color
        self.drawer = drawer

    @abstractmethod
    def draw(self) -> None:
        pass
