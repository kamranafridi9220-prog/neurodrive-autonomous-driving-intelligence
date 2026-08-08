import pygame
import math

# ---------------------------------------------------------
# NeuroDrive - Autonomous Driving Intelligence System
# Day 1: Lightweight Vehicle Simulation
# ---------------------------------------------------------

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NeuroDrive - Autonomous Driving Laboratory")

clock = pygame.time.Clock()

# Vehicle state
car_x = WIDTH // 2
car_y = HEIGHT - 120

car_width = 42
car_height = 75

speed = 0.0
max_speed = 6.0
acceleration = 0.12
braking = 0.20

steering = 0.0
max_steering = 3.0

# Road
road_left = 250
road_right = 750
road_center = WIDTH // 2

font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 17)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # -----------------------------------------------------
    # VEHICLE CONTROL
    # -----------------------------------------------------

    if keys[pygame.K_UP]:
        speed += acceleration

    if keys[pygame.K_DOWN]:
        speed -= braking

    if keys[pygame.K_LEFT]:
        steering = -max_steering

    elif keys[pygame.K_RIGHT]:
        steering = max_steering

    else:
        steering *= 0.8

    speed = max(-2.0, min(speed, max_speed))

    # Natural resistance
    if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
        speed *= 0.985

    # Vehicle movement
    car_x += steering * (abs(speed) / max_speed)

    # Keep vehicle inside road
    car_x = max(
        road_left + car_width // 2,
        min(car_x, road_right - car_width // 2)
    )

    # -----------------------------------------------------
    # DRAW ENVIRONMENT
    # -----------------------------------------------------

    screen.fill((45, 120, 55))

    # Road
    pygame.draw.rect(
        screen,
        (55, 55, 60),
        (road_left, 0, road_right - road_left, HEIGHT)
    )

    # Road edges
    pygame.draw.line(
        screen,
        (240, 240, 240),
        (road_left, 0),
        (road_left, HEIGHT),
        5
    )

    pygame.draw.line(
        screen,
        (240, 240, 240),
        (road_right, 0),
        (road_right, HEIGHT),
        5
    )

    # Centre lane markings
    for y in range(-50, HEIGHT, 100):
        pygame.draw.rect(
            screen,
            (240, 220, 70),
            (road_center - 4, y, 8, 55)
        )

    # -----------------------------------------------------
    # DRAW VEHICLE
    # -----------------------------------------------------

    car_rect = pygame.Rect(
        car_x - car_width // 2,
        car_y - car_height // 2,
        car_width,
        car_height
    )

    pygame.draw.rect(
        screen,
        (30, 150, 240),
        car_rect,
        border_radius=8
    )

    # Windshield
    pygame.draw.rect(
        screen,
        (170, 220, 245),
        (
            car_rect.x + 7,
            car_rect.y + 10,
            car_width - 14,
            18
        ),
        border_radius=4
    )

    # -----------------------------------------------------
    # TELEMETRY
    # -----------------------------------------------------

    speed_display = round(speed * 10, 1)

    title = font.render(
        "NEURODRIVE AUTONOMOUS DRIVING LAB",
        True,
        (255, 255, 255)
    )

    telemetry = small_font.render(
        f"Speed: {speed_display} km/h   "
        f"Steering: {steering:.2f}   "
        f"Lane Position: {car_x:.0f}",
        True,
        (255, 255, 255)
    )

    mode = small_font.render(
        "MANUAL CONTROL | Arrow Keys = Drive",
        True,
        (255, 230, 100)
    )

    screen.blit(title, (20, 20))
    screen.blit(telemetry, (20, 55))
    screen.blit(mode, (20, 82))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
