import pygame
import sys
import time
import random

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 30
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
MINE_COUNT = 10
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Fonts
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# Load images
flag_img = pygame.image.load("assets/images/flag.png")
mine_img = pygame.image.load("assets/images/mine.png")
flag_img = pygame.transform.scale(flag_img, (GRID_SIZE, GRID_SIZE))
mine_img = pygame.transform.scale(mine_img, (GRID_SIZE, GRID_SIZE))

# Game state
def initialize_game():
    global grid, revealed, mines, game_over
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    revealed = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    mines = []
    game_over = False

    # Generate random mine locations
    while len(mines) < MINE_COUNT:
        x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in mines:
            mines.append((x, y))
            grid[y][x] = -1

    # Calculate adjacent mine counts
    for x, y in mines:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x + dx < GRID_WIDTH and 0 <= y + dy < GRID_HEIGHT and grid[y + dy][x + dx] != -1:
                    grid[y + dy][x + dx] += 1

initialize_game()

# Game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                x, y = event.pos
                cell_x, cell_y = x // GRID_SIZE, y // GRID_SIZE
                if not revealed[cell_y][cell_x]:
                    revealed[cell_y][cell_x] = True
                    if grid[cell_y][cell_x] == -1:
                        game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
                x, y = event.pos
                cell_x, cell_y = x // GRID_SIZE, y // GRID_SIZE
                if not revealed[cell_y][cell_x]:
                    revealed[cell_y][cell_x] = True
                    if grid[cell_y][cell_x] == -1:
                        game_over = True
    if game_over:
        # Check for "Play Again" click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            x, y = event.pos
            if (WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100) and (HEIGHT // 2 <= y <= HEIGHT // 2 + 40):
                initialize_game()

    # Draw the grid
    screen.fill(WHITE)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)
            if revealed[y][x]:
                if grid[y][x] == -1:
                    screen.blit(mine_img, rect.topleft)
                elif grid[y][x] > 0:
                    text = font.render(str(grid[y][x]), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
            elif game_over:
                if grid[y][x] == -1:
                    pygame.draw.circle(screen, RED, rect.center, GRID_SIZE // 2)
                elif grid[y][x] > 0:
                    text = font.render(str(grid[y][x]), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
            else:
                screen.blit(flag_img, rect.topleft)

    if game_over:
        text = game_over_font.render("Game Over", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(text, text_rect)
        play_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 40)
        pygame.draw.rect(screen, GRAY, play_again_button)
        play_again_text = font.render("Play Again", True, BLACK)
        play_again_text_rect = play_again_text.get_rect(center=play_again_button.center)
        screen.blit(play_again_text, play_again_text_rect)

    pygame.display.flip()
    pygame.time.delay(1000 // FPS)

pygame.quit()
sys.exit()
