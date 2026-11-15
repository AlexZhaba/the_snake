"""Игра «Змейка»"""

import sys

import pygame as pg

from constants import (BOARD_BACKGROUND_COLOR, BORDER_COLOR,
                       DEFAULT_SNAKE_POSITION, DOWN, GRID_HEIGHT, GRID_SIZE,
                       GRID_WIDTH, KEY_DIRECTION_MAP, LEFT, RIGHT,
                       SCREEN_HEIGHT, SCREEN_SIZE, SCREEN_WIDTH, SPEED, UP)
from model.apple import Apple
from model.game_object import GameObject
from model.pygame_drawer import PyGameDrawer
from model.snake import Snake

__all__ = [
    'Apple', 'GameObject', 'BOARD_BACKGROUND_COLOR', 'PyGameDrawer', 'Snake',
    'SCREEN_WIDTH', 'SCREEN_HEIGHT', 'GRID_SIZE', 'GRID_WIDTH', 'GRID_HEIGHT',
    'UP', 'DOWN', 'LEFT', 'RIGHT', 'BORDER_COLOR', 'SPEED', 'clock', 'screen',
    'KEY_DIRECTION_MAP', 'DEFAULT_SNAKE_POSITION', 'handle_keys', 'main',
]

clock = pg.time.Clock()
screen = pg.Surface(SCREEN_SIZE)


def handle_keys(snake: Snake) -> None:
    """Обрабатываем выход и один поворот за кадр"""
    direction_changed = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif (
            not direction_changed
            and event.type == pg.KEYDOWN
            and event.key in KEY_DIRECTION_MAP
        ):
            new_direction, opposite_direction = KEY_DIRECTION_MAP[event.key]
            if snake.direction != opposite_direction:
                snake.next_direction = new_direction
                direction_changed = True


def main():
    """Запускаем игру"""
    global screen
    drawer = PyGameDrawer(SCREEN_SIZE, GRID_SIZE)
    screen = drawer.screen
    snake = Snake(DEFAULT_SNAKE_POSITION, drawer=drawer)
    apple = Apple(snake.positions, drawer=drawer)
    drawer.fill_all_area()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        _, next_head = snake.get_next_move()
        eating = next_head == apple.position
        body = list(snake.positions)
        if not eating:
            body.pop()

        if next_head in body:
            snake.reset(DEFAULT_SNAKE_POSITION)
            if apple.position in snake.positions:
                apple.randomize_position(snake.positions)
        else:
            snake.move(with_extend=eating)
            if eating:
                if snake.length == GRID_WIDTH * GRID_HEIGHT:
                    snake.reset(DEFAULT_SNAKE_POSITION)
                apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        drawer.update_area()


if __name__ == '__main__':
    main()
