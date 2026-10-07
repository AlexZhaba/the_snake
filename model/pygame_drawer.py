from functools import cache
from typing import override

import pygame
from pygame import Surface

from model.game_object import BodyColor, Drawer, Position

BOARD_BACKGROUND_COLOR = (0, 0, 0)


class PyGameDrawer(Drawer):
    """Отрисовка поля через Pygame. Здесь просто добавил возможность потенциально поменять drawer чтобы запустить
    игру в консоли, например.
    """

    screen: Surface
    grid_size: int
    coordinates: tuple[int, int]

    def __init__(self, coordinates: tuple[int, int], grid_size: int) -> None:
        _ = pygame.init()
        self.screen = pygame.display.set_mode(coordinates, 0, 32)
        pygame.display.set_caption("Змейка")
        self.grid_size = grid_size
        self.coordinates = coordinates

    @override
    def rect(self, position: Position, size: tuple[int, int], color: BodyColor) -> None:
        """Переводим клетки в пиксели и рисуем прямоугольник."""
        rect = pygame.Rect(
            (position[0] * self.grid_size, position[1] * self.grid_size),
            (size[0] * self.grid_size, size[1] * self.grid_size),
        )
        _ = pygame.draw.rect(self.screen, color, rect)

    @override
    def get_grid_size(self) -> tuple[int, int]:
        """Размер поля в клетках."""
        return (
            self.coordinates[0] // self.grid_size,
            self.coordinates[1] // self.grid_size,
        )

    @override
    def clear(self, position: Position, size: tuple[int, int]) -> None:
        """Стираем клетки, закрашивая их цветом фона."""
        return self.rect(
            position,
            size,
            BOARD_BACKGROUND_COLOR,
        )

    @override
    def fill_all_area(self) -> None:
        """Закрашиваем всё поле цветом фона."""
        self.screen.fill(BOARD_BACKGROUND_COLOR)

    @override
    def update_area(self) -> None:
        """Показываем то, что нарисовали."""
        pygame.display.flip()


@cache
def get_default_drawer() -> PyGameDrawer:
    """Создаём отрисовщик один раз и потом используем его же."""
    return PyGameDrawer((640, 480), 20)
