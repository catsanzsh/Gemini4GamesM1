import pygame
import sys
import random
import time
import numpy as np
import os

# NO SDL_VIDEODRIVER setting for Rosetta

# --- Constants ---
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = GRID_SIZE * GRID_WIDTH
HEIGHT = GRID_SIZE * GRID_HEIGHT
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
INITIAL_SNAKE_LENGTH = 3
INITIAL_SNAKE_SPEED = 10
SAMPLE_RATE = 44100

# --- Sound Functions ---
def generate_beep(frequency, duration, volume=0.5):
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), False)
    wave = volume * np.sin(2 * np.pi * frequency * t)
    wave = np.int16(wave * 32767)
    return pygame.mixer.Sound(wave.tobytes())

def generate_boop(frequency, duration, volume=0.5):
    t = np.linspace(0, duration, int(duration * SAMPLE_RATE), False)
    wave = volume * np.sign(np.sin(2 * np.pi * frequency * t))
    wave = np.int16(wave * 32767)
    return pygame.mixer.Sound(wave.tobytes())

# --- Pygame Initialization ---
pygame.init()

# --- Sound Initialization ---
pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1)
food_sound = generate_beep(880, 0.1)
game_over_sound = generate_boop(220, 0.5)
move_sound = generate_beep(440, 0.02, 0.2)

# --- Game Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meowser Snake")
clock = pygame.time.Clock()

# --- Helper Functions ---
def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y))

def draw_snake(snake):
    for segment in snake:
        rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, SNAKE_COLOR, rect)

def draw_food(food):
    rect = pygame.Rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, FOOD_COLOR, rect)

def generate_food(snake):
    while True:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food not in snake:
            return food

def display_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(text, (10, 10))

def game_over_screen(score):
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, 50)
    game_over_text = font.render("Game Over!", True, TEXT_COLOR)
    score_text = font.render(f"Final Score: {score}", True, TEXT_COLOR)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()
    game_over_sound.play()
    time.sleep(3)

# --- Game Logic ---
def run_game():
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    for i in range(1, INITIAL_SNAKE_LENGTH):
        snake.append((snake[0][0] - i, snake[0][1]))

    direction = (1, 0)
    food = generate_food(snake)
    score = 0
    speed = INITIAL_SNAKE_SPEED
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)
        move_sound.play()

        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
            or new_head in snake[1:]
        ):
            game_over_screen(score)
            return

        if new_head == food:
            food = generate_food(snake)
            score += 1
            speed += 0.5
            food_sound.play()
        else:
            snake.pop()

        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        display_score(score)
        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
