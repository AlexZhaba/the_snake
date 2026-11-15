"""Интерфейс отрисовки"""

from typing import Protocol

type Position = tuple[int, int]
type BodyColor = tuple[int, int, int]


class Drawer(Protocol):
    """Что нужно уметь отрисовщику"""

    def rect(
        self, position: Position, size: tuple[int, int], color: BodyColor
    ) -> None:
        """Рисуем прямоугольник по клеткам"""

    def get_grid_size(self) -> tuple[int, int]:
        """Размер поля в клетках"""

    def clear(self, position: Position, size: tuple[int, int]) -> None:
        """Стираем прямоугольник"""

    def fill_all_area(self) -> None:
        """Очищаем поле"""

    def update_area(self) -> None:
        """Показываем нарисованное"""
