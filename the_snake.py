import pygame

from model.apple import Apple
from model.game_object import GameObject, Position  # noqa: F401
from model.pygame_drawer import BOARD_BACKGROUND_COLOR  # noqa: F401
from model.pygame_drawer import PyGameDrawer
from model.snake import Snake

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BORDER_COLOR = (93, 216, 228)

SPEED = 20

# Настройка времени:
clock = pygame.time.Clock()
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


# Кнопка, новое направление и противоположное ему.
KEY_DIRECTION_MAP = {
    pygame.K_UP: (UP, DOWN),
    pygame.K_DOWN: (DOWN, UP),
    pygame.K_LEFT: (LEFT, RIGHT),
    pygame.K_RIGHT: (RIGHT, LEFT),
}

DEFAULT_SNAKE_POSITION: list[Position] = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]


def handle_keys(game_object: Snake) -> None:
    """Обрабатываем выход и один поворот за кадр."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN and event.key in KEY_DIRECTION_MAP:
            new_direction, opposite_direction = KEY_DIRECTION_MAP[event.key]
            if game_object.direction != opposite_direction:
                game_object.update_direction(new_direction)
                break


def main():
    """Запускаем игру."""
    global screen
    # Инициализация PyGame:
    drawer = PyGameDrawer((SCREEN_WIDTH, SCREEN_HEIGHT), GRID_SIZE)
    screen = drawer.screen
    # Создаём змейку и яблоко.

    snake = Snake(DEFAULT_SNAKE_POSITION, drawer)
    apple = Apple.create_at_random_place(drawer)

    drawer.fill_all_area()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        _, next_snake_head_position = snake.get_next_move()

        intersection_with_apple = next_snake_head_position == apple.position
        collision_positions = list(snake.get_positions())
        if not intersection_with_apple:
            collision_positions.pop()

        if next_snake_head_position in collision_positions:
            snake.reset(DEFAULT_SNAKE_POSITION)
            _, next_snake_head_position = snake.get_next_move()
            intersection_with_apple = (
                next_snake_head_position == apple.position
            )

        if intersection_with_apple:
            apple = Apple.create_at_random_place(drawer)

        snake.move(with_extend=intersection_with_apple)

        snake.draw()
        apple.draw()
        drawer.update_area()


if __name__ == "__main__":
    main()
