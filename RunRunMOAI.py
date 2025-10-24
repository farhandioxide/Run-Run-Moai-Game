import pygame
import sys
import os

# Asset base path for PyInstaller
BASE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Initialize
pygame.init()

# Screen size
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run! Run! MOAI!!")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load assets
player_img = pygame.image.load(os.path.join(BASE_PATH, "assets/player.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (24, 38))
obstacle_img = pygame.image.load(os.path.join(BASE_PATH, "assets/obstacle.png")).convert_alpha()
obstacle_img = pygame.transform.scale(obstacle_img, (29, 44))
bg_img = pygame.image.load(os.path.join(BASE_PATH, "assets/background.png")).convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# Fonts
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 80)

# Player setup
player_x = 100
player_y = 300
player_y_change = 0
is_jumping = False

# Obstacle
obstacle_x = 800
obstacle_y = 268

# Score
score = 0
high_score = 0

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def main_menu():
    while True:
        screen.fill(color=BLACK)
        draw_text("Run! Run! MOAI!!", big_font, WHITE, 220, 50)
        draw_text("Ekti Kutta Mara Dour Game!!", font, RED, 280, 110)
        draw_text("[SPACE] - New Game", font, WHITE, 280, 150)
        draw_text("[H] - High Score", font, WHITE, 280, 200)
        draw_text("[C] - Credits", font, WHITE, 280, 250)
        draw_text("[ESC] - Exit", font, WHITE, 280, 300)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                if event.key == pygame.K_h:
                    show_high_score()
                if event.key == pygame.K_c:
                    show_credits()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def show_high_score():
    while True:
        screen.fill(WHITE)
        draw_text("High Score", big_font, BLACK, 270, 100)
        draw_text(f"{high_score}", big_font, RED, 370, 180)
        draw_text("[ESC] - Back", font, BLACK, 300, 300)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

def show_credits():
    while True:
        screen.fill(WHITE)
        draw_text("Illust. and Dev. by Farhan Dioxide", font, BLACK, 240, 180)
        draw_text("[ESC] - Back", font, BLACK, 300, 300)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

def game_loop():
    global player_y, player_y_change, is_jumping, obstacle_x, score, high_score

    player_y = 274
    player_y_change = 0
    is_jumping = False
    obstacle_x = 800
    score = 0

    running = True
    while running:
        screen.blit(bg_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    player_y_change = -15
                    is_jumping = True

        # Jump physics
        player_y += player_y_change
        if is_jumping:
            player_y_change += 1
        if player_y >= 274:
            player_y = 274
            is_jumping = False

        # Obstacle movement
        obstacle_x -= 6
        if obstacle_x < -50:
            obstacle_x = 800
            score += 1
            if score > high_score:
                high_score = score

        # Draw player & obstacle
        screen.blit(player_img, (player_x, player_y))
        screen.blit(obstacle_img, (obstacle_x, obstacle_y))

        # Score
        draw_text(f"Score: {score}", font, BLACK, 10, 10)

        # Collision detection
        player_rect = pygame.Rect(player_x, player_y, 24, 38)
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, 29, 44)
        if player_rect.colliderect(obstacle_rect):
            game_over()
            running = False

        pygame.display.update()
        clock.tick(FPS)

def game_over():
    draw_text("Game Over", big_font, RED, 280, 130)
    draw_text("Press R to Retry or ESC to Menu", font, BLACK, 200, 230)
    pygame.display.update()
    pygame.time.delay(1000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    main_menu()

# Start the game
main_menu()
