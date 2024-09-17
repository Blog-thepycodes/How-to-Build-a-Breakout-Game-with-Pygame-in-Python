import pygame
import random
import time
 
 
# Initialize pygame
pygame.init()
 
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 
 
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
PURPLE = (160, 32, 240)
 
 
# Paddle dimensions
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10
PADDLE_DEFAULT_LENGTH = 100  # Default paddle length
 
 
# Ball dimensions
BALL_RADIUS = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
 
 
# Brick dimensions
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 50
 
 
# Font
FONT = pygame.font.SysFont('Arial', 36)
BUTTON_FONT = pygame.font.SysFont('Arial', 28)
 
 
# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game - The Pycodes")
 
 
# Initialize paddle
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
 
 
# Initialize ball
ball_x = SCREEN_WIDTH // 2
ball_y = paddle_y - BALL_RADIUS  # Start ball on top of paddle
ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))
ball_on_paddle = True  # The ball starts on the paddle
 
 
# Initialize bricks
bricks = []
level = 1  # Initial level
lives = 3  # Player starts with 3 lives
score = 0  # Start score
 
 
# Power-ups
active_powerups = []
POWERUP_TYPES = ['expand_paddle', 'slow_ball', 'extra_life']
powerup_effect_time = {}  # Store the start time of each active power-up
 
 
# Create bricks
def create_bricks():
  global bricks
  bricks = []
  rows = level + 5  # Number of rows increases with level
  for row in range(rows):
      for col in range(10):
          brick_x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
          brick_y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_OFFSET_TOP
          bricks.append([brick_x, brick_y, random.choice([GREEN, BLUE, RED]), False])
 
 
def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()
 
 
  # Draw button
  if x + width > mouse[0] > x and y + height > mouse[1] > y:
      pygame.draw.rect(screen, active_color, (x, y, width, height))
      if click[0] == 1 and action is not None:
          action()  # Call the action (restart_game in this case)
  else:
      pygame.draw.rect(screen, inactive_color, (x, y, width, height))
 
 
  # Render button text
  button_text = FONT.render(text, True, BLACK)
  screen.blit(button_text, ((x + (width // 2 - button_text.get_width() // 2)), (y + (height // 2 - button_text.get_height() // 2))))
 
 
# Game Over Screen with button click detection
def game_over_screen(score):
  game_over = True
  while game_over:
      screen.fill(BLACK)
      game_over_text = FONT.render('Game Over', True, WHITE)
      score_text = FONT.render(f'Final Score: {score}', True, WHITE)
      screen.blit(game_over_text, ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 3))
      screen.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, SCREEN_HEIGHT // 3 + 50))
 
 
      # Draw the restart button
      draw_button("Restart Game", (SCREEN_WIDTH - 200) // 2, SCREEN_HEIGHT // 2, 200, 60, GRAY, WHITE, restart_game)
 
 
      pygame.display.update()
 
 
      # Event handling
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              quit()
 
 
# Congratulations Screen
def congratulations_screen():
  screen.fill(BLACK)
  congrats_text = FONT.render('Congratulations!', True, WHITE)
  win_text = FONT.render('You Won the Game!', True, WHITE)
  screen.blit(congrats_text, ((SCREEN_WIDTH - congrats_text.get_width()) // 2, SCREEN_HEIGHT // 3))
  screen.blit(win_text, ((SCREEN_WIDTH - win_text.get_width()) // 2, SCREEN_HEIGHT // 3 + 50))
 
 
  draw_button("Play Again", (SCREEN_WIDTH - 200) // 2, SCREEN_HEIGHT // 2, 200, 60, GRAY, WHITE, restart_game)
  pygame.display.update()
 
 
def restart_game():
  global game_running, game_over, score, level, lives, game_started, active_powerups, powerup_effect_time, ball_on_paddle
  score = 0
  level = 1
  lives = 3
  game_running = True
  game_over = False
  game_started = True
  ball_on_paddle = True
  active_powerups.clear()
  powerup_effect_time.clear()
  reset_game(life_lost=False)
 
 
  # This will bring us back to the main game loop
  game_loop()
 
 
# Reset game entities
def reset_game(life_lost=False):
  global ball_x, ball_y, ball_speed_x, ball_speed_y, paddle_x, paddle_y, ball_on_paddle
  ball_x = paddle_x + PADDLE_WIDTH // 2
  ball_y = paddle_y - BALL_RADIUS  # Reset ball on paddle
  ball_speed_x = (BALL_SPEED_X + level - 1) * random.choice((1, -1))  # Increase ball speed with level
  ball_speed_y = -(BALL_SPEED_Y + level - 1)  # Reset ball speed
  ball_on_paddle = True  # Ball starts on paddle again
  paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
 
 
  if not life_lost:  # Only reset bricks when starting a new level or game
      create_bricks()
 
 
# Start Screen
def start_screen():
  screen.fill(BLACK)
  title_text = FONT.render('Breakout Game - The Pycodes', True, WHITE)
  screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, SCREEN_HEIGHT // 3))
 
 
  draw_button("Start Game", (SCREEN_WIDTH - 200) // 2, SCREEN_HEIGHT // 2, 200, 60, GRAY, WHITE, start_game)
  pygame.display.update()
 
 
# Start or Restart the game
def start_game():
  global game_running, game_over, game_started, score
  score = 0  # Initialize score when the game starts
  game_running = True
  game_over = False
  game_started = True  # Set this to True to start the game
  reset_game()
 
 
# Power-up logic
def generate_powerup(x, y):
  if random.random() < 0.2:  # 20% chance to generate a power-up
      powerup_type = random.choice(POWERUP_TYPES)
      active_powerups.append([x, y, powerup_type, time.time()])
 
 
def handle_powerups():
   global paddle_x, paddle_y, PADDLE_WIDTH, ball_speed_x, ball_speed_y, lives
   for powerup in active_powerups[:]:
       x, y, powerup_type, start_time = powerup
 
 
       # Draw power-ups with correct colors
       if powerup_type == 'extra_life':
           pygame.draw.rect(screen, YELLOW, (x, y, 20, 20))  # Extra Life (Yellow)
       elif powerup_type == 'expand_paddle':
           pygame.draw.rect(screen, GREEN, (x, y, 20, 20))  # Expand Paddle (Green)
       elif powerup_type == 'slow_ball':
           pygame.draw.rect(screen, PURPLE, (x, y, 20, 20))  # Slow Ball (Purple)
 
 
       # Move power-up downwards
       powerup[1] += 5
 
 
       # Check for collision with paddle
       if paddle_y < y + 20 < paddle_y + PADDLE_HEIGHT and paddle_x < x < paddle_x + PADDLE_WIDTH:
           if powerup_type == 'expand_paddle':
               PADDLE_WIDTH = PADDLE_DEFAULT_LENGTH + 50  # Extend paddle length
               powerup_effect_time[powerup_type] = time.time()
           elif powerup_type == 'slow_ball':
               ball_speed_x *= 0.5
               ball_speed_y *= 0.5
               powerup_effect_time[powerup_type] = time.time()
           elif powerup_type == 'extra_life':
               lives += 1
           active_powerups.remove(powerup)
 
 
       # Revert power-up effects after 30 seconds
       for p_type in list(powerup_effect_time.keys()):
           if time.time() - powerup_effect_time[p_type] >= 30:
               if p_type == 'expand_paddle':
                   PADDLE_WIDTH = PADDLE_DEFAULT_LENGTH  # Revert paddle to default length
               elif p_type == 'slow_ball':
                   ball_speed_x = (BALL_SPEED_X + level - 1) * random.choice((1, -1))  # Revert ball speed
                   ball_speed_y = -(BALL_SPEED_Y + level - 1)
               del powerup_effect_time[p_type]
 
 
# Main game loop
def game_loop():
  global ball_x, ball_y, ball_speed_x, ball_speed_y, paddle_x, paddle_y, lives, score, game_running, game_started, ball_on_paddle, level
 
 
  # Reset game state
  create_bricks()
  reset_game()
 
 
  while game_running:
      screen.fill(BLACK)
 
 
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              game_running = False
 
 
      # Paddle movement
      keys = pygame.key.get_pressed()
      if keys[pygame.K_LEFT]:
          paddle_x -= PADDLE_SPEED
      if keys[pygame.K_RIGHT]:
          paddle_x += PADDLE_SPEED
 
 
      # Keep paddle within screen bounds
      if paddle_x < 0:
          paddle_x = 0
      if paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
          paddle_x = SCREEN_WIDTH - PADDLE_WIDTH
 
 
      # Ball movement and collision handling
      if not ball_on_paddle:
          ball_x += ball_speed_x
          ball_y += ball_speed_y
 
 
      # Ball collision with walls
      if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= SCREEN_WIDTH:
          ball_speed_x = -ball_speed_x
      if ball_y - BALL_RADIUS <= 0:
          ball_speed_y = -ball_speed_y
 
 
      # Ball collision with paddle
      if paddle_y < ball_y + BALL_RADIUS < paddle_y + PADDLE_HEIGHT and paddle_x < ball_x < paddle_x + PADDLE_WIDTH:
          ball_speed_y = -ball_speed_y
 
 
      # Ball falling below paddle (life lost)
      if ball_y > SCREEN_HEIGHT:
          lives -= 1
          if lives == 0:
              game_running = False
              game_over_screen(score)
              return
          reset_game(life_lost=True)
 
 
      # Brick collision detection
      for brick in bricks[:]:
          brick_x, brick_y, brick_color, hit = brick
          if brick_x < ball_x < brick_x + BRICK_WIDTH and brick_y < ball_y < brick_y + BRICK_HEIGHT:
              ball_speed_y = -ball_speed_y
              bricks.remove(brick)
              score += 10
              generate_powerup(brick_x, brick_y)
              break
 
 
      # Check for win condition
      if not bricks:
          if level < 5:
              level += 1
              create_bricks()
              reset_game()
          else:
              game_running = False
              congratulations_screen()
              return
 
 
      # Draw bricks
      for brick in bricks:
          pygame.draw.rect(screen, brick[2], (brick[0], brick[1], BRICK_WIDTH, BRICK_HEIGHT))
 
 
      # Draw paddle
      pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
 
 
      # Draw ball
      pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)
 
 
      # Handle power-ups
      handle_powerups()
 
 
      # Display score and lives
      score_text = FONT.render(f'Score: {score}', True, WHITE)
      lives_text = FONT.render(f'Lives: {lives}', True, WHITE)
      level_text = FONT.render(f'Level: {level}', True, WHITE)
      screen.blit(score_text, (20, 10))
      screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 20, 10))
      screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 10))
 
 
      # Ball on paddle logic (for start of game or life lost)
      if ball_on_paddle:
          ball_x = paddle_x + PADDLE_WIDTH // 2
          if keys[pygame.K_SPACE]:
              ball_on_paddle = False
 
 
      # Update the display
      pygame.display.update()
 
 
      # Frame rate control
      pygame.time.Clock().tick(60)
 
 
# Main program
game_running = False
game_started = False
 
 
while not game_started:
  start_screen()
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          game_running = False
          game_started = True  # To exit the outer loop
 
 
if game_running:
  game_loop()
 
pygame.quit()
