"""Отрисовка игры через Pygame"""

from functools import cache
from typing import override

import pygame as pg

from constants import (BOARD_BACKGROUND_COLOR, GRID_SIZE, SCREEN_DEPTH,
                       SCREEN_SIZE)
from model.drawer import BodyColor, Drawer, Position


class PyGameDrawer(Drawer):
    """Отрисовка поля через Pygame"""

    screen: pg.Surface
    grid_size: int
    coordinates: tuple[int, int]

    def __init__(self, coordinates: tuple[int, int], grid_size: int) -> None:
        """Создаём окно и задаём размер клетки"""
        _ = pg.init()
        self.screen = pg.display.set_mode(coordinates, 0, SCREEN_DEPTH)
        pg.display.set_caption('Змейка')
        self.grid_size = grid_size
        self.coordinates = coordinates

    @override
    def rect(
        self, position: Position, size: tuple[int, int], color: BodyColor
    ) -> None:
        """Переводим клетки в пиксели и рисуем прямоугольник"""
        rect = pg.Rect(
            (position[0] * self.grid_size, position[1] * self.grid_size),
            (size[0] * self.grid_size, size[1] * self.grid_size),
        )
        _ = pg.draw.rect(self.screen, color, rect)

    @override
    def get_grid_size(self) -> tuple[int, int]:
        """Размер поля в клетках"""
        return (
            self.coordinates[0] // self.grid_size,
            self.coordinates[1] // self.grid_size,
        )

    @override
    def clear(self, position: Position, size: tuple[int, int]) -> None:
        """Стираем клетки, закрашивая их цветом фона"""
        return self.rect(
            position,
            size,
            BOARD_BACKGROUND_COLOR,
        )

    @override
    def fill_all_area(self) -> None:
        """Закрашиваем всё поле цветом фона"""
        self.screen.fill(BOARD_BACKGROUND_COLOR)

    @override
    def update_area(self) -> None:
        """Показываем то, что нарисовали"""
        pg.display.update()


@cache
def get_default_drawer() -> PyGameDrawer:
    """Создаём отрисовщик один раз и потом используем его же"""
    return PyGameDrawer(SCREEN_SIZE, GRID_SIZE)
