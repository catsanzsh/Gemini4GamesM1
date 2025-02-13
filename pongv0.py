import pygame
import random
import numpy as np  # Import numpy

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)  # Initialize mixer *before* defining sounds


# --- Sound Functions ---

def beep(frequency, duration):
    """Generates a simple sine wave beep."""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    wave = (wave * 32767).astype(np.int16)  # Convert to 16-bit PCM
    sound = pygame.mixer.Sound(wave)
    sound.play()

def boop(frequency, duration):
    """Generates a sine wave with a faster decay."""
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    # Sine wave with an exponential decay
    wave = 0.5 * np.sin(2 * np.pi * frequency * t) * np.exp(-5 * t)
    wave = (wave * 32767).astype(np.int16)  # Convert to 16-bit PCM
    sound = pygame.mixer.Sound(wave)
    sound.play()



# --- Constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 10
PADDLE_SPEED = 5
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# --- Classes ---

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PADDLE_SPEED

    def move_up(self):
        self.rect.y -= self.speed
        if self.rect.top < 0:
            self.rect.top = 0

    def move_down(self):
        self.rect.y += self.speed
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, size, x, y):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top and bottom walls
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y *= -1
            boop(600, 0.1) # Play sound on wall bounce

        # Bounce off left and right (scoring) - handled in main loop

    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        # Randomize initial direction
        self.speed_x = BALL_SPEED_X * random.choice((1, -1))
        self.speed_y = BALL_SPEED_Y * random.choice((1, -1))
        



# --- Game Setup ---

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Create paddles
player1_paddle = Paddle(WHITE, PADDLE_WIDTH, PADDLE_HEIGHT, 50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
player2_paddle = Paddle(WHITE, PADDLE_WIDTH, PADDLE_HEIGHT, SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)

# Create ball
ball = Ball(WHITE, BALL_SIZE, SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2)
ball.reset()  # To get initial random direction

# Sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player1_paddle)
all_sprites.add(player2_paddle)
all_sprites.add(ball)

# --- Game Loop ---

running = True
clock = pygame.time.Clock()
player1_score = 0
player2_score = 0

# Font for score display
font = pygame.font.Font(None, 74)  # Default system font, size 74

while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Player Input ---
    keys = pygame.key.get_pressed()

    # Player 1 Controls (W and S)
    if keys[pygame.K_w]:
        player1_paddle.move_up()
    if keys[pygame.K_s]:
        player1_paddle.move_down()

    # Player 2 Controls (Up and Down Arrows)
    if keys[pygame.K_UP]:
        player2_paddle.move_up()
    if keys[pygame.K_DOWN]:
        player2_paddle.move_down()


    # --- Game Logic ---

    # Ball movement and collision
    ball.update()

    # Paddle-ball collisions
    if pygame.sprite.collide_rect(ball, player1_paddle):
        ball.speed_x *= -1
        beep(440, 0.05)  # Play sound on paddle hit

    if pygame.sprite.collide_rect(ball, player2_paddle):
        ball.speed_x *= -1
        beep(440, 0.05)


    # Scoring and ball reset
    if ball.rect.left < 0:
        player2_score += 1
        ball.reset()
        beep(220, 0.2)  # Play a lower sound on scoring
    elif ball.rect.right > SCREEN_WIDTH:
        player1_score += 1
        ball.reset()
        beep(220, 0.2)

    # --- Drawing ---
    screen.fill(BLACK)

    # Draw sprites
    all_sprites.draw(screen)
    
    # Display scores
    score_text = font.render(str(player1_score) + "  " + str(player2_score), True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width()//2 , 10))

    # --- Update Display ---
    pygame.display.flip()

    # --- Frame Rate ---
    clock.tick(60)  # 60 frames per second

# --- Quit Pygame ---
pygame.quit()
