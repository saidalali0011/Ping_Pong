# --- IMPORTS ---
import pygame
import sys
import time

#for test working ... 
from paddle_logic import move_paddle

# --- CONSTANTS ---
# Using all-caps names for constants is a Python convention.
# This makes the code much cleaner and easier to adjust.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_START_X = 350 # Horizontal distance from the center for the paddles
PADDLE_SPEED = 20 # How many pixels the paddle moves per key press
BALL_SIZE = 20
BALL_START_DX = 2.7 # Initial horizontal speed of the ball (delta x)
BALL_START_DY = 2.7 # Initial vertical speed of the ball (delta y)
SCORE_FONT_SIZE = 24 # Font size for score display
BALL_COLLISION_RANGE = 40 # Range for ball collision with paddle

# Colors
BLUE = (0, 100, 255)
RED = (255, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (25, 25, 112) # midnight blue

# --- PYGAME INITIALIZATION ---
# Initialize PyGame with error handling
try:
    pygame.init()
    wind = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PING PONG Game - by SAID ")   #the title of the game window
    clock =pygame.time.Clock()
    
    # Try to load preferred font with fallback to default
    try:
        score_font = pygame.font.SysFont("courier", SCORE_FONT_SIZE, bold=True)  #choosing the settings of the font 
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
    } #y : for basics and logic of moving , rect: drawing the racket
    return paddle

# --- GAME OBJECTS ---
# Create Rackets using the helper function
racket1 = create_paddle(-PADDLE_START_X + SCREEN_WIDTH // 2, BLUE) # Player 1 paddle # 50 for x
racket2 = create_paddle(PADDLE_START_X + SCREEN_WIDTH // 2 - PADDLE_WIDTH, RED) # Player 2  paddle #750 -20 =730

# Ball / dictionary
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

# Score tracking variables
score1 = 0
score2 = 0

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
        
        if ball['rect'].bottom >= SCREEN_HEIGHT:  # Check collision with the bottom wall
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
            
            # Increase ball speed slightly after paddle hit
            if ball['dx'] > 0:
                ball['dx'] += 0.05
            else:
                ball['dx'] -= 0.05
                
            if ball['dy'] > 0:
                ball['dy'] += 0.05
            else:
                ball['dy'] -= 0.05

        # Collision with Racket 1 (Left Paddle)
        if (ball['rect'].left <= racket1['rect'].right and ball['rect'].left >= racket1['rect'].right - 10) :
            
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
