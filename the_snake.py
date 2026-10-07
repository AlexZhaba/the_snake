import pygame

from model.apple import Apple
from model.game_object import Position
from model.pygame_drawer import PyGameDrawer
from model.snake import Snake

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
KEY_DIRECTION_MAP = {
    pygame.K_UP: (UP, DOWN),
    pygame.K_DOWN: (DOWN, UP),
    pygame.K_LEFT: (LEFT, RIGHT),
    pygame.K_RIGHT: (RIGHT, LEFT),
}

DEFAULT_SNAKE_POSITION: list[Position] = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]


def main():
    # Инициализация PyGame:
    drawer = PyGameDrawer((SCREEN_WIDTH, SCREEN_HEIGHT), GRID_SIZE)
    # Тут нужно создать экземпляры классов.

    snake = Snake(DEFAULT_SNAKE_POSITION, drawer)
    apple = Apple.create_at_random_place(drawer)

    drawer.fill_all_area()
    while True:
        clock.tick(SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN and event.key in KEY_DIRECTION_MAP:
                new_direction, opposite_direction = KEY_DIRECTION_MAP[event.key]
                if snake.direction != opposite_direction:
                    snake.update_direction(new_direction)

        _, next_snake_head_position = snake.get_next_move()

        if len(snake.get_intersection_with([next_snake_head_position])) != 0:
            snake.reset(DEFAULT_SNAKE_POSITION)

        intersection_with_apple = False
        if len(apple.get_intersection_with([next_snake_head_position])) != 0:
            intersection_with_apple = True
            apple = Apple.create_at_random_place(drawer)

        snake.move(with_extend=intersection_with_apple)

        snake.draw()
        apple.draw()
        drawer.update_area()


if __name__ == "__main__":
    main()
