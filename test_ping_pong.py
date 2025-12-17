import pytest
from unittest.mock import Mock
from paddle_logic import move_paddle, SCREEN_HEIGHT, PADDLE_HEIGHT

# Заглушка для pygame.Rect
MockRect = Mock 

def test_move_paddle_up_within_bounds():
    paddle = {
        'y': 50,
        'speed': 20,
        'rect': MockRect(y=50)
    }
    move_paddle(paddle, -1)
    assert paddle['y'] == 30
    assert paddle['rect'].y == 30

def test_move_paddle_down_within_bounds():
    paddle = {
        'y': 50,
        'speed': 20,
        'rect': MockRect(y=50)
    }
    move_paddle(paddle, 1)
    assert paddle['y'] == 70
    assert paddle['rect'].y == 70

def test_move_paddle_up_exceeds_top_boundary():
    paddle = {
        'y': 5,
        'speed': 20,
        'rect': MockRect(y=5)
    }
    move_paddle(paddle, -1)
    assert paddle['y'] == 0
    assert paddle['rect'].y == 0

def test_move_paddle_down_exceeds_bottom_boundary():
    max_y = SCREEN_HEIGHT - PADDLE_HEIGHT
    paddle = {
        'y': max_y + 10,
        'speed': 20,
        'rect': MockRect(y=max_y + 10)
    }
    move_paddle(paddle, 1)
    assert paddle['y'] == max_y
    assert paddle['rect'].y == max_y

def test_move_paddle_at_bottom_edge():
    max_y = SCREEN_HEIGHT - PADDLE_HEIGHT
    paddle = {
        'y': max_y,
        'speed': 20,
        'rect': MockRect(y=max_y)
    }
    move_paddle(paddle, 1)
    assert paddle['y'] == max_y
    assert paddle['rect'].y == max_y

def test_move_paddle_at_top_edge():
    paddle = {
        'y': 0,
        'speed': 20,
        'rect': MockRect(y=0)
    }
    move_paddle(paddle, -1)
    assert paddle['y'] == 0
    assert paddle['rect'].y == 0

def test_move_paddle_zero_direction():
    paddle = {
        'y': 100,
        'speed': 20,
        'rect': MockRect(y=100)
    }
    move_paddle(paddle, 0)
    assert paddle['y'] == 100
    assert paddle['rect'].y == 100

def test_move_paddle_negative_speed():
    paddle = {
        'y': 50,
        'speed': -20,
        'rect': MockRect(y=50)
    }
    move_paddle(paddle, 1)
    assert paddle['y'] == 30
    assert paddle['rect'].y == 30

def test_move_paddle_rect_is_updated():
    paddle = {
        'y': 40,
        'speed': 15,
        'rect': MockRect()
    }
    move_paddle(paddle, 1)
    assert paddle['rect'].y == paddle['y']