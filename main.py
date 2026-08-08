import pygame

# ---------------------------------------------------------
# NeuroDrive - Autonomous Driving Intelligence System
# Day 1: Autonomous Lane-Keeping Prototype
# ---------------------------------------------------------

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NeuroDrive - Autonomous Driving Laboratory")

clock = pygame.time.Clock()

# ---------------------------------------------------------
# ROAD CONFIGURATION
# ---------------------------------------------------------

road_left = 250
road_right = 750
road_center = WIDTH // 2

left_lane_center = (road_left + road_center) // 2
right_lane_center = (road_center + road_right) // 2

# NeuroDrive will follow the right lane
target_lane_center = right_lane_center

# ---------------------------------------------------------
# VEHICLE STATE
# ---------------------------------------------------------

car_x = float(target_lane_center)
car_y = HEIGHT - 120

car_width = 42
car_height = 75

speed = 0.0
max_speed = 6.0

acceleration = 0.12
braking = 0.20

steering = 0.0
max_steering = 3.0

# ---------------------------------------------------------
# AUTONOMOUS CONTROLLER
# ---------------------------------------------------------

autonomous_mode = False

target_speed = 4.0

# Proportional controller strength
steering_gain = 0.045

lane_error = 0.0

# Used to create the illusion of forward road movement
road_scroll = 0.0

# ---------------------------------------------------------
# FONTS
# ---------------------------------------------------------

font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 17)
status_font = pygame.font.SysFont("Arial", 19, bold=True)

running = True

while running:

    # -----------------------------------------------------
    # EVENTS
    # -----------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Switch between manual and autonomous driving
            if event.key == pygame.K_a:
                autonomous_mode = not autonomous_mode

            # Reset vehicle
            if event.key == pygame.K_r:
                car_x = float(target_lane_center)
                speed = 0.0
                steering = 0.0

    keys = pygame.key.get_pressed()

    # -----------------------------------------------------
    # MANUAL CONTROL
    # -----------------------------------------------------

    if not autonomous_mode:

        if keys[pygame.K_UP]:
            speed += acceleration

        if keys[pygame.K_DOWN]:
            speed -= braking

        if keys[pygame.K_LEFT]:
            steering = -max_steering

        elif keys[pygame.K_RIGHT]:
            steering = max_steering

        else:
            steering *= 0.80

        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            speed *= 0.985

    # -----------------------------------------------------
    # AUTONOMOUS DRIVING CONTROLLER
    # -----------------------------------------------------

    else:

        # Calculate how far the vehicle is from lane centre
        lane_error = target_lane_center - car_x

        # Convert lane-position error into steering command
        steering = lane_error * steering_gain

        # Prevent excessive steering
        steering = max(
            -max_steering,
            min(steering, max_steering)
        )

        # Autonomous speed controller
        if speed < target_speed:
            speed += acceleration

        elif speed > target_speed + 0.15:
            speed -= braking

        # Reduce speed if lane error becomes large
        if abs(lane_error) > 90:
            speed *= 0.97

    # -----------------------------------------------------
    # VEHICLE PHYSICS
    # -----------------------------------------------------

    speed = max(-2.0, min(speed, max_speed))

    car_x += steering * (abs(speed) / max_speed)

    # Keep vehicle inside road boundaries
    car_x = max(
        road_left + car_width // 2,
        min(car_x, road_right - car_width // 2)
    )

    # Road movement simulation
    road_scroll += speed * 2.5

    if road_scroll >= 100:
        road_scroll = 0

    # Always calculate lane error for telemetry
    lane_error = target_lane_center - car_x

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

    # Moving centre lane markings
    for y in range(-100, HEIGHT + 100, 100):

        moving_y = int(y + road_scroll)

        pygame.draw.rect(
            screen,
            (240, 220, 70),
            (road_center - 4, moving_y, 8, 55)
        )

    # -----------------------------------------------------
    # TARGET LANE VISUALISATION
    # -----------------------------------------------------

    # Lane-centre reference line
    pygame.draw.line(
        screen,
        (80, 180, 255),
        (target_lane_center, 110),
        (target_lane_center, HEIGHT),
        2
    )

    # Target marker
    pygame.draw.circle(
        screen,
        (80, 180, 255),
        (target_lane_center, 130),
        8
    )

    # -----------------------------------------------------
    # DRAW VEHICLE
    # -----------------------------------------------------

    car_rect = pygame.Rect(
        int(car_x - car_width // 2),
        int(car_y - car_height // 2),
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

    # Sensor connection between car and target lane centre
    if autonomous_mode:

        pygame.draw.line(
            screen,
            (120, 220, 255),
            (int(car_x), int(car_y - car_height // 2)),
            (target_lane_center, int(car_y - 100)),
            2
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
        f"Lane Position: {car_x:.0f}   "
        f"Lane Error: {lane_error:.1f}",
        True,
        (255, 255, 255)
    )

    if autonomous_mode:

        mode_text = "AUTONOMOUS MODE | NeuroDrive controlling vehicle"

        mode = status_font.render(
            mode_text,
            True,
            (80, 255, 120)
        )

    else:

        mode_text = "MANUAL MODE | Arrow Keys = Drive | A = Activate Autonomy"

        mode = status_font.render(
            mode_text,
            True,
            (255, 230, 100)
        )

    instructions = small_font.render(
        "A = Toggle Autonomy    R = Reset Vehicle",
        True,
        (220, 220, 220)
    )

    sensor_text = small_font.render(
        f"Target Lane Centre: {target_lane_center} px",
        True,
        (120, 210, 255)
    )

    screen.blit(title, (20, 20))
    screen.blit(telemetry, (20, 55))
    screen.blit(mode, (20, 84))
    screen.blit(instructions, (20, 112))
    screen.blit(sensor_text, (20, 140))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
