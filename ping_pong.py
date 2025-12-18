# --- IMPORTS ---
import pygame
import sys
import time

#for test working ... 
from paddle_logic import move_paddle

# --- CONSTANTS --- Using all-caps names for constants is a Python convention.
SCREEN_WIDTH = 800
"""
Width of the game window in pixels.
:type: int
"""
SCREEN_HEIGHT = 600
"""
Height of the game window in pixels.
:type: int
"""
PADDLE_WIDTH = 20
"""
Width of the paddle (racket) in pixels.
:type: int
"""
PADDLE_HEIGHT = 100
"""
Height of the paddle (racket) in pixels.
:type: int
"""
PADDLE_START_X = 350 
"""
Horizontal distance from the center of the window to the initial paddle position in pixels.

:type: int
""" 
PADDLE_SPEED = 20
"""
Paddle movement speed in pixels per key press.
:type: int
"""
BALL_SIZE = 20
"""
Diameter of the ball in pixels.
:type: int
"""
BALL_START_DX = 2.7
"""
Initial horizontal speed of the ball (change in X-axis per frame).
:type: float
"""
BALL_START_DY = 2.7
"""
Initial vertical speed of the ball (change in Y-axis per frame).
:type: float
"""
SCORE_FONT_SIZE = 24
"""
Font size for displaying the score in points.
:type: int
"""
BALL_COLLISION_RANGE = 40
"""
Additional vertical zone around the paddle for detecting ball collision in pixels.
:type: int 
"""

# Colors
BLUE = (0, 100, 255)
"""
Red,Green ,Blue (RGB) color for Player 1's paddle.
:type: tuple[int, int, int]
"""
RED = (255, 50, 50)
"""
RGB color for Player 2's paddle.
:type: tuple[int, int, int]
"""
WHITE = (255, 255, 255)
"""
RGB color for the ball, score text, and center line.
:type: tuple[int, int, int]
"""
BLACK = (0, 0, 0)
"""
RGB color (black). Used as background or auxiliary color.
:type: tuple[int, int, int]
"""
BG_COLOR = (25, 25, 112)
"""
Main background color of the game window in RGB (dark blue shade).
:type: tuple[int, int, int]
"""

# ---Initialize PyGame with error handling---
try:
    pygame.init()
    wind = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    """
    Main PyGame window/surface object for rendering all game graphics.
    
    Created during PyGame initialization with specified screen dimensions.
    All drawing operations are performed on this surface.
    
    :type: pygame.Surface
    """
    pygame.display.set_caption("PING PONG Game - by SAID ")   #the title of the game window
    clock =pygame.time.Clock()
    """
    PyGame Clock object for controlling game frame rate.
    
    Used to maintain consistent frame rate (60 FPS) and timing.
    
    :type: pygame.time.Clock
    """

    # Try to load preferred font with fallback to default
    try:
        score_font = pygame.font.SysFont("courier", SCORE_FONT_SIZE, bold=True)  
        """
        Font object for rendering score text on screen.
        
        Primary font is "courier" with specified size and bold style.
        Falls back to default system font if courier is unavailable.
        
        :type: pygame.font.Font
        """    
    except Exception as font_error:   # Fallback to default font if courier is not available
        print(f"Font warning: Could not load 'courier'. Using default. Error: {font_error}")
        score_font = pygame.font.SysFont(None, SCORE_FONT_SIZE)
    
except pygame.error as init_error: # Handle PyGame initialization failure (this excep. is for the first try init())
    print(f"FATAL ERROR: Failed to initialize PyGame.")
    print(f"Error details: {init_error}")
    print("Please install PyGame with: pip install pygame")
    sys.exit(1)  # Exit with error code

# --- HELPER FUNCTION FOR OBJECT CREATION ---
def create_paddle(x_pos, color):
    """
    Creates a paddle rectangle with specified position and color
    
    :param x_pos: X-coordinate position of the paddle
    :type x_pos: int
    :param color: Color of the paddle
    :type color: tuple
    :returns: Dictionary containing paddle properties
    """
    paddle = {
        'rect': pygame.Rect(x_pos, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2 , 
                          PADDLE_WIDTH, PADDLE_HEIGHT), #for x , 250 pix ,20 , 100 #position of paddle 
        'color': color,
        'speed': PADDLE_SPEED,
        'y': SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
    } #y : for basics and logic of moving , 'rect': drawing the racket and it is a key for the dictionary
    return paddle

# --- GAME OBJECTS ---
# Create Rackets using the helper function
racket1 = create_paddle(-PADDLE_START_X + SCREEN_WIDTH // 2, BLUE)
"""
Paddle for Player 1 (left side).

Created using the create_paddle() helper function.

- Positioned on the left side of the screen
- Controlled using W/S keys
- Blue color

:type: dict
:ivar rect: pygame.Rect object representing paddle position and dimensions
:type rect: pygame.Rect
:ivar color: RGB color tuple (blue)
:type color: tuple[int, int, int]
:ivar speed: Movement speed in pixels
:type speed: int
:ivar y: Current Y-coordinate position (for movement logic)
:type y: int 
-350+400=50
"""

racket2 = create_paddle(PADDLE_START_X + SCREEN_WIDTH // 2 - PADDLE_WIDTH, RED)
"""
Paddle (racket) for Player 2 (right side).

Created using the create_paddle() helper function.

- Positioned on the right side of the screen
- Controlled using UP/DOWN arrow keys
- Red color

:type: dict
:ivar rect: pygame.Rect object representing paddle position and dimensions
:type rect: pygame.Rect
:ivar color: RGB color tuple (red)
:type color: tuple[int, int, int]
:ivar speed: Movement speed in pixels
:type speed: int
:ivar y: Current Y-coordinate position (for movement logic)
:type y: int 
""" #750 -20 =730

ball = {
    'rect': pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2,
                       SCREEN_HEIGHT // 2 - BALL_SIZE // 2,
                       BALL_SIZE, BALL_SIZE),
    'color': WHITE,
    'dx': BALL_START_DX, # horizontal movement
    'dy': BALL_START_DY, # vertical movement
    'x': SCREEN_WIDTH // 2,
    'y': SCREEN_HEIGHT // 2
}
"""
Game ball object stored as a dictionary.

Represents the ping pong ball with position, movement, and visual properties.
Starts at the center of the screen.

:type: dict
:ivar rect: pygame.Rect object representing ball position and dimensions
:type rect: pygame.Rect
:ivar color: RGB color tuple (white)
:type color: tuple[int, int, int]
:ivar dx: Horizontal velocity (change in x-position per frame)
:type dx: float
:ivar dy: Vertical velocity (change in y-position per frame)
:type dy: float
:ivar x: Current X-coordinate position (center point)
:type x: int
:ivar y: Current Y-coordinate position (center point)
:type y: int
"""

# Score tracking variables
score1 = 0
"""
Current score for Player 1 (left paddle).

Incremented when the ball passes the right side of the screen.

:type: int
"""

score2 = 0
"""
Current score for Player 2 (right paddle).

Incremented when the ball passes the left side of the screen.

:type: int
"""

# --- FUNCTIONS ---
def draw_paddle(paddle):
    """Draws a paddle on the screen"""
    pygame.draw.rect(wind, paddle['color'], paddle['rect'])

def draw_ball():
    """Draws the ball on the screen"""
    pygame.draw.ellipse(wind, ball['color'], ball['rect'])

def draw_score():
    """Draws the score on the screen"""
    score_text = f"Player 1: {score1} | Player 2: {score2}"
    score_surface = score_font.render(score_text, True, WHITE) # true to ten3im the letters
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 40)) #40 = 40 pix from the north
    wind.blit(score_surface, score_rect)

def reset_ball():
    """Resets the ball to center with initial speed when losing"""
    ball['rect'].center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball['dx'] = BALL_START_DX
    ball['dy'] = BALL_START_DY

# --- MAIN GAME LOOP ---
running = True
"""
Main game loop control flag.

When set to True, the game continues running.
When set to False, the game loop ends and the program exits.

:type: bool
"""
try:
    while running:
        # Handle events with error checking
        try:
            for event in pygame.event.get():   #every thing the user do it (event)
                if event.type == pygame.QUIT:
                    running = False
        except Exception as event_error:
            print(f"Event handling error: {event_error}") # Continue running despite event error
        
        # Get keyboard input , and error handling
        try:
            keys = pygame.key.get_pressed()
            """
            Current state of all keyboard keys.
            
            A list-like object where each index corresponds to a pygame key constant.
            Each element is True if the key is currently pressed, False otherwise.
            Updated each frame to capture real-time keyboard input.
            
            :type: list[bool]
            """            
        except Exception as key_error:
            print(f"Keyboard input error: {key_error}")
            keys = []  # Use empty list , because key should always work(we caleed it)
        
        # Player 1 controls (W/S) 
        if keys[pygame.K_w]:
            move_paddle(racket1, -1) 
        if keys[pygame.K_s]:
            move_paddle(racket1, 1)   
        
        # Player 2 controls (Up/Down Arrows) 
        if keys[pygame.K_UP]:
            move_paddle(racket2, -1)  
        if keys[pygame.K_DOWN]:
            move_paddle(racket2, 1)  
        
        # Move the ball with error handling (like dx not a nb)
        try:
            ball['rect'].x += ball['dx'] #location of ball +speed dx
            ball['rect'].y += ball['dy']
        except (TypeError, KeyError) as ball_error:
            print(f"Ball movement error: {ball_error}. Resetting ball.")
            reset_ball()
        
        # Top and Bottom Wall Collision (Bouncing)
        if ball['rect'].top <= 0:  # Check collision with the top wall
            ball['rect'].top = 0
            ball['dy'] *= -1  # Reverse the vertical direction (bounce)
        # Check collision with the bottom wall
        if ball['rect'].bottom >= SCREEN_HEIGHT:  
            ball['rect'].bottom = SCREEN_HEIGHT
            ball['dy'] *= -1  # Reverse the vertical direction (bounce)

        # Side Wall Collision (Scoring) with error handling
        if ball['rect'].right >= SCREEN_WIDTH:  # Check if the ball goes past the right side
            try:
                score1 += 1  # Player 1 scores a point
                reset_ball()
                ball['dx'] *= -1  # Reverse direction to serve to the other side
                time.sleep(0.5)  # Short pause before continuing
            except Exception as score_error:
                print(f"Scoring error (right side): {score_error}")
                # Continue game despite scoring error

        # Check if the ball goes past the left side        
        if ball['rect'].left <= 0:  
            try:
                score2 += 1  # Player 2 scores a point
                reset_ball()
                ball['dx'] *= -1  # Reverse direction to serve to the other side
                time.sleep(0.5)  # Short pause before continuing
            except Exception as score_error:
                print(f"Scoring error (left side): {score_error}")
                # Continue game despite scoring error

        # Paddle Collision
        # Collision with Racket 2 (Right Paddle)
        if (ball['rect'].right >= racket2['rect'].left and 
            ball['rect'].right <= racket2['rect'].left + 10) and \
           (ball['rect'].centery > racket2['rect'].top - BALL_COLLISION_RANGE and 
            ball['rect'].centery < racket2['rect'].bottom + BALL_COLLISION_RANGE):
            
            ball['rect'].right = racket2['rect'].left  # Ensure the ball doesn't get stuck
            ball['dx'] *= -1  # Reverse the horizontal direction (bounce)

        # Collision with Racket 1 (Left Paddle)
        if (ball['rect'].left <= racket1['rect'].right and 
            ball['rect'].left >= racket1['rect'].right - 10) and \
            (ball['rect'].centery > racket1['rect'].top - BALL_COLLISION_RANGE and 
            ball['rect'].centery < racket1['rect'].bottom + BALL_COLLISION_RANGE):
            
            ball['rect'].left = racket1['rect'].right  # Ensure the ball doesn't get stuck
            ball['dx'] *= -1  # Reverse the horizontal direction (bounce)
            
            # # Increase ball speed slightly after paddle hit
            # if ball['dx'] > 0:  # Check if ball is moving to the right
            #     ball['dx'] += 0.05  # Increase rightward speed by 0.05
            # else:  # Ball is moving to the left
            #     ball['dx'] -= 0.05  # Increase leftward speed by 0.05 (negative value)
                
            # if ball['dy'] > 0:  # Check if ball is moving upward
            #     ball['dy'] += 0.05  # Increase upward speed by 0.05
            # else:  # Ball is moving downward
            #     ball['dy'] -= 0.05  # Increase downward speed by 0.05 (negative value)
        
        # Draw everything with error handling
        try:
            wind.fill(BG_COLOR)  # Set background color
            
            # Draw center line
            for y in range(0, SCREEN_HEIGHT, 30):
                pygame.draw.rect(wind, WHITE, (SCREEN_WIDTH // 2 - 2, y, 4, 15))
            
            draw_paddle(racket1)
            draw_paddle(racket2)
            draw_ball()
            draw_score()
        except pygame.error as draw_error:
            print(f"Drawing error: {draw_error}")
            # Try to continue, but might need to exit
        
        # Update display with error handling
        try:
            pygame.display.flip()
        except pygame.error as display_error:
            print(f"Display update error: {display_error}")
            running = False  # Stop game if display fails
        
        # Control frame rate with error handling
        
        clock.tick(60)


except Exception as main_game_error:
    # Handle critical errors in main game loop
    print(f"CRITICAL: Game loop crashed with error: {main_game_error}")
    
finally:
    # This code (finally) always runs, even if an error occurs
    print("Game session ended.")
    print(f"Final score: Player 1: {score1} | Player 2: {score2}")

# Quit PyGame clearly and end the code
pygame.quit()
sys.exit()  
