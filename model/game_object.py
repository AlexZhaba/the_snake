from collections import deque
from typing import Protocol

type Position = tuple[int, int]
type BodyColor = tuple[int, int, int]


class Drawer(Protocol):
    """Что нужно уметь отрисовщику для игры."""

    def rect(self, position: Position, size: tuple[int, int], color: BodyColor) -> None:
        """Рисуем прямоугольник по координатам клеток."""
        ...

    def get_grid_size(self) -> tuple[int, int]:
        """Размер поля в клетках."""
        ...

    def clear(self, position: Position, size: tuple[int, int]) -> None:
        """Стираем прямоугольник на поле."""
        ...

    def fill_all_area(self) -> None:
        """Закрашиваем всё поле цветом фона."""
        ...

    def update_area(self) -> None:
        """Показываем то, что нарисовали."""
        ...


class GameObject:
    """Общее для объектов игры: клетки, цвет и отрисовщик.
    В задании было указано использование position в качестве параметра для GameObject,
    и в тестах проверялось, поэтому пришлось добавить геттер. Но кажется, что более правильно
    именно описывать несколько позиций на уровне объекта. например, камень может быть изогнутой
    формы буквы Г, или квадратом 2x2, я бы хотел переиспользовать функции коллизии именно со списком
    positions
    """

    positions: deque[Position]
    body_color: BodyColor
    drawer: Drawer

    def __init__(
        self,
        positions: list[Position] | None = None,
        body_color: BodyColor = (0, 255, 0),
        drawer: Drawer | None = None,
    ) -> None:
        if drawer is None:
            from model.pygame_drawer import get_default_drawer

            drawer = get_default_drawer()
        if positions is None:
            width, height = drawer.get_grid_size()
            positions = [(width // 2, height // 2)]
        # deque позволяет удалять хвост и добавлять голову за O(1).
        self.positions = deque(positions)
        self.body_color = body_color
        self.drawer = drawer

    @property
    def position(self) -> Position:
        """Первая клетка объекта."""
        return self.positions[0]

    @position.setter
    def position(self, position: Position) -> None:
        self.positions[0] = position

    def draw(self) -> None:
        """Рисуем все клетки объекта."""
        for position in self.positions:
            self.drawer.rect(position, (1, 1), self.body_color)

    def get_positions(self) -> deque[Position]:
        """Возвращаем очередь клеток объекта."""
        return self.positions

    def get_intersection_with(self, positions: list[Position]) -> set[Position]:
        """Проверяем, какие клетки совпали с переданными."""
        intersection = set(self.get_positions()) & set(positions)

        return intersection
