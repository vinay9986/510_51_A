import pygame
import random
import sys

# Constants
WIDTH, HEIGHT = 600, 400  # Small window
FPS = 60
SHIP_SPEED = 5
BULLET_SPEED = -8
ASTEROID_SPEED = 2
ASTEROID_SPAWN_DELAY = 1000  # milliseconds

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Shooter")
clock = pygame.time.Clock()

# Fonts
font_small = pygame.font.SysFont(None, 20)
font_big = pygame.font.SysFont(None, 36)

# Ship setup
ship_width, ship_height = 40, 20
ship = pygame.Rect(WIDTH // 2 - ship_width // 2, HEIGHT - ship_height - 10, ship_width, ship_height)

# Game entities
bullets = []
asteroids = []

# Timers
pygame.time.set_timer(pygame.USEREVENT, ASTEROID_SPAWN_DELAY)

score = 0
running = True
while running:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_SPACE:
                # Fire bullet
                bullet_rect = pygame.Rect(ship.centerx - 2, ship.top - 10, 4, 10)
                bullets.append(bullet_rect)
        elif event.type == pygame.USEREVENT:
            # Spawn asteroid at random x
            asteroid_size = random.randint(20, 40)
            asteroid_rect = pygame.Rect(random.randint(0, WIDTH - asteroid_size), -asteroid_size, asteroid_size, asteroid_size)
            asteroids.append(asteroid_rect)

    # Handle continuous key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship.left > 0:
        ship.x -= SHIP_SPEED
    if keys[pygame.K_RIGHT] and ship.right < WIDTH:
        ship.x += SHIP_SPEED
    if keys[pygame.K_UP] and ship.top > 0:
        ship.y -= SHIP_SPEED
    if keys[pygame.K_DOWN] and ship.bottom < HEIGHT:
        ship.y += SHIP_SPEED

    # Update bullets
    for bullet in bullets[:]:
        bullet.y += BULLET_SPEED
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Update asteroids
    for asteroid in asteroids[:]:
        asteroid.y += ASTEROID_SPEED
        if asteroid.top > HEIGHT:
            asteroids.remove(asteroid)

    # Collision detection
    for asteroid in asteroids[:]:
        # Bullet collisions
        for bullet in bullets[:]:
            if asteroid.colliderect(bullet):
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                score += 1
                break
        # Ship collision
        if asteroid.colliderect(ship):
            running = False

    # Drawing
    screen.fill(BLACK)
    # Draw ship
    pygame.draw.rect(screen, GREEN, ship)
    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)
    # Draw asteroids
    for asteroid in asteroids:
        pygame.draw.rect(screen, RED, asteroid)

    # Draw HUD
    controls_text = "Controls: Arrow keys move | Space: shoot | Q: quit"
    score_text = f"Score: {score}"
    controls_surface = font_small.render(controls_text, True, WHITE)
    score_surface = font_big.render(score_text, True, WHITE)
    screen.blit(controls_surface, (10, 5))
    screen.blit(score_surface, (10, 25))

    pygame.display.flip()

pygame.quit()
sys.exit()
