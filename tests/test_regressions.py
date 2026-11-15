"""Проверки сброса змейки и обработки событий."""

from unittest.mock import patch

import pygame
import pytest


def test_reset_restores_initial_state(_the_snake):
    """После сброса змейка снова короткая и движется вправо."""
    snake = _the_snake.Snake()
    snake.move(with_extend=True)
    snake.update_direction(_the_snake.UP)
    old_positions = list(snake.positions)

    snake.reset(_the_snake.DEFAULT_SNAKE_POSITION)

    assert snake.length == 1
    assert list(snake.positions) == _the_snake.DEFAULT_SNAKE_POSITION
    assert snake.direction == _the_snake.RIGHT
    assert snake.old_positions == old_positions


def test_quit_after_turn_is_not_lost(_the_snake):
    """Закрытие обрабатывается и после поворота в том же кадре."""
    snake = _the_snake.Snake()
    events = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP),
        pygame.event.Event(pygame.QUIT),
    ]
    with patch.object(pygame.event, 'get', return_value=events):
        with patch.object(pygame, 'quit') as quit_game:
            with pytest.raises(SystemExit):
                _the_snake.handle_keys(snake)
    quit_game.assert_called_once_with()


def test_only_one_turn_per_frame(_the_snake):
    """Несколько клавиш не позволяют развернуться назад за кадр."""
    snake = _the_snake.Snake()
    events = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT),
    ]
    with patch.object(pygame.event, 'get', return_value=events):
        _the_snake.handle_keys(snake)
    assert snake.direction == _the_snake.UP
