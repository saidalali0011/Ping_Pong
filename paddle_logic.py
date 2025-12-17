# --- CONSTANTS (копируем из основного файла) ---
SCREEN_HEIGHT = 600
PADDLE_HEIGHT = 100


def move_paddle(paddle, direction):
    """
    Moves a paddle vertically by specified direction.

    :param paddle: The paddle dictionary to move
    :type paddle: dict
    :param direction: Direction of movement (1 for down, -1 for up)
    :type direction: int
    """
    paddle['y'] += direction * paddle['speed']

    # Boundary check
    max_y = SCREEN_HEIGHT - PADDLE_HEIGHT
    min_y = 0

    if paddle['y'] > max_y:
        paddle['y'] = max_y
    elif paddle['y'] < min_y:
        paddle['y'] = min_y

    # Sync rect.y with paddle['y']
    paddle['rect'].y = paddle['y']