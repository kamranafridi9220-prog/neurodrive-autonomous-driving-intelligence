import pygame

# =========================================================
# NeuroDrive - Autonomous Driving Intelligence System
# Day 2: Lane Keeping + Obstacle Detection + Emergency Brake
# =========================================================

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "NeuroDrive - Autonomous Driving Laboratory"
)

clock = pygame.time.Clock()

# =========================================================
# ROAD CONFIGURATION
# =========================================================

road_left = 250
road_right = 750
road_center = WIDTH // 2

left_lane_center = (road_left + road_center) // 2
right_lane_center = (road_center + road_right) // 2

target_lane_center = right_lane_center

# =========================================================
# EGO VEHICLE
# =========================================================

car_x = float(target_lane_center)
car_y = HEIGHT - 110

car_width = 42
car_height = 75

speed = 0.0
max_speed = 6.0

acceleration = 0.08
braking = 0.18
emergency_braking = 0.32

steering = 0.0
max_steering = 3.0

# =========================================================
# AUTONOMOUS CONTROLLER
# =========================================================

autonomous_mode = False

cruise_speed = 4.0
target_speed = cruise_speed

steering_gain = 0.045

lane_error = 0.0

road_scroll = 0.0

# =========================================================
# OBSTACLE VEHICLE
# =========================================================

obstacle_width = 46
obstacle_height = 80

obstacle_x = float(target_lane_center)
obstacle_y = 80.0

# Simulated obstacle travel
obstacle_motion_speed = 0.7

# =========================================================
# SENSOR / SAFETY SYSTEM
# =========================================================

front_distance = 999.0

risk_state = "CLEAR"

safe_distance = 260
caution_distance = 190
brake_distance = 125
emergency_distance = 70

sensor_active = False

# =========================================================
# FONTS
# =========================================================

font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 17)
status_font = pygame.font.SysFont(
    "Arial",
    19,
    bold=True
)

running = True

while running:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Toggle autonomous mode
            if event.key == pygame.K_a:
                autonomous_mode = not autonomous_mode

            # Reset simulation
            if event.key == pygame.K_r:

                car_x = float(target_lane_center)
                speed = 0.0
                steering = 0.0

                obstacle_x = float(target_lane_center)
                obstacle_y = 80.0

                risk_state = "CLEAR"

    keys = pygame.key.get_pressed()

    # =====================================================
    # MANUAL MODE
    # =====================================================

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

    # =====================================================
    # AUTONOMOUS MODE
    # =====================================================

    else:

        # -------------------------------------------------
        # Lane keeping
        # -------------------------------------------------

        lane_error = target_lane_center - car_x

        steering = lane_error * steering_gain

        steering = max(
            -max_steering,
            min(steering, max_steering)
        )

        # -------------------------------------------------
        # FRONT SENSOR
        # -------------------------------------------------

        lateral_difference = abs(
            car_x - obstacle_x
        )

        same_lane = lateral_difference < 70

        if same_lane and obstacle_y < car_y:

            sensor_active = True

            front_distance = (
                car_y
                - obstacle_y
                - obstacle_height / 2
                - car_height / 2
            )

        else:

            sensor_active = False
            front_distance = 999

        # -------------------------------------------------
        # RISK ASSESSMENT
        # -------------------------------------------------

        if front_distance <= emergency_distance:

            risk_state = "EMERGENCY"

            target_speed = 0.0

        elif front_distance <= brake_distance:

            risk_state = "BRAKE"

            target_speed = 1.0

        elif front_distance <= caution_distance:

            risk_state = "CAUTION"

            target_speed = 2.2

        else:

            risk_state = "CLEAR"

            target_speed = cruise_speed

        # -------------------------------------------------
        # SPEED CONTROLLER
        # -------------------------------------------------

        if risk_state == "EMERGENCY":

            speed -= emergency_braking

        elif speed < target_speed:

            speed += acceleration

        elif speed > target_speed:

            speed -= braking

        # Additional safety reduction
        if abs(lane_error) > 100:

            speed *= 0.97

    # =====================================================
    # PHYSICS
    # =====================================================

    speed = max(
        0.0,
        min(speed, max_speed)
    )

    car_x += steering * (
        abs(speed) / max_speed
    )

    car_x = max(
        road_left + car_width // 2,
        min(
            car_x,
            road_right - car_width // 2
        )
    )

    lane_error = target_lane_center - car_x

    # Road animation
    road_scroll += speed * 2.5

    if road_scroll >= 100:
        road_scroll = 0

    # =====================================================
    # OBSTACLE MOVEMENT
    # =====================================================

    if autonomous_mode:

        relative_motion = (
            speed * 0.55
            - obstacle_motion_speed
        )

        obstacle_y += max(
            relative_motion,
            0.4
        )

    # Respawn obstacle after passing
    if obstacle_y > HEIGHT + 100:

        obstacle_y = -100
        obstacle_x = float(
            target_lane_center
        )

    # =====================================================
    # DRAW ENVIRONMENT
    # =====================================================

    screen.fill(
        (45, 120, 55)
    )

    # Road
    pygame.draw.rect(
        screen,
        (55, 55, 60),
        (
            road_left,
            0,
            road_right - road_left,
            HEIGHT
        )
    )

    # Road boundaries
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

    # Centre road markings
    for y in range(
        -100,
        HEIGHT + 100,
        100
    ):

        moving_y = int(
            y + road_scroll
        )

        pygame.draw.rect(
            screen,
            (240, 220, 70),
            (
                road_center - 4,
                moving_y,
                8,
                55
            )
        )

    # =====================================================
    # TARGET LANE
    # =====================================================

    pygame.draw.line(
        screen,
        (80, 180, 255),
        (
            target_lane_center,
            170
        ),
        (
            target_lane_center,
            HEIGHT
        ),
        2
    )

    # =====================================================
    # OBSTACLE VEHICLE
    # =====================================================

    obstacle_rect = pygame.Rect(
        int(
            obstacle_x
            - obstacle_width / 2
        ),
        int(
            obstacle_y
            - obstacle_height / 2
        ),
        obstacle_width,
        obstacle_height
    )

    pygame.draw.rect(
        screen,
        (220, 70, 70),
        obstacle_rect,
        border_radius=8
    )

    # Obstacle windshield
    pygame.draw.rect(
        screen,
        (245, 180, 180),
        (
            obstacle_rect.x + 7,
            obstacle_rect.y + 10,
            obstacle_width - 14,
            18
        ),
        border_radius=4
    )

    # =====================================================
    # EGO VEHICLE
    # =====================================================

    car_rect = pygame.Rect(
        int(
            car_x
            - car_width / 2
        ),
        int(
            car_y
            - car_height / 2
        ),
        car_width,
        car_height
    )

    pygame.draw.rect(
        screen,
        (30, 150, 240),
        car_rect,
        border_radius=8
    )

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

    # =====================================================
    # FRONT SENSOR VISUALISATION
    # =====================================================

    if autonomous_mode and sensor_active:

        pygame.draw.line(
            screen,
            (255, 220, 80),
            (
                int(car_x),
                int(
                    car_y
                    - car_height / 2
                )
            ),
            (
                int(obstacle_x),
                int(
                    obstacle_y
                    + obstacle_height / 2
                )
            ),
            3
        )

    # =====================================================
    # SAFETY ZONES
    # =====================================================

    if autonomous_mode:

        # Emergency zone
        pygame.draw.line(
            screen,
            (255, 70, 70),
            (
                int(car_x - 75),
                int(car_y - emergency_distance)
            ),
            (
                int(car_x + 75),
                int(car_y - emergency_distance)
            ),
            3
        )

        # Brake zone
        pygame.draw.line(
            screen,
            (255, 170, 60),
            (
                int(car_x - 85),
                int(car_y - brake_distance)
            ),
            (
                int(car_x + 85),
                int(car_y - brake_distance)
            ),
            2
        )

        # Caution zone
        pygame.draw.line(
            screen,
            (255, 230, 80),
            (
                int(car_x - 95),
                int(car_y - caution_distance)
            ),
            (
                int(car_x + 95),
                int(car_y - caution_distance)
            ),
            2
        )

    # =====================================================
    # TELEMETRY
    # =====================================================

    speed_display = round(
        speed * 10,
        1
    )

    title = font.render(
        "NEURODRIVE AUTONOMOUS DRIVING LAB",
        True,
        (255, 255, 255)
    )

    telemetry = small_font.render(
        f"Speed: {speed_display} km/h   "
        f"Steering: {steering:.2f}   "
        f"Lane Error: {lane_error:.1f}",
        True,
        (255, 255, 255)
    )

    # -----------------------------------------------------
    # Risk colour
    # -----------------------------------------------------

    if risk_state == "CLEAR":

        risk_colour = (
            80,
            255,
            120
        )

    elif risk_state == "CAUTION":

        risk_colour = (
            255,
            230,
            80
        )

    elif risk_state == "BRAKE":

        risk_colour = (
            255,
            160,
            60
        )

    else:

        risk_colour = (
            255,
            70,
            70
        )

    if autonomous_mode:

        mode = status_font.render(
            "AUTONOMOUS MODE",
            True,
            (80, 255, 120)
        )

    else:

        mode = status_font.render(
            "MANUAL MODE | Press A for Autonomy",
            True,
            (255, 230, 100)
        )

    distance_text = small_font.render(
        f"Front Distance: "
        f"{front_distance:.0f} px",
        True,
        (220, 220, 220)
    )

    risk_text = status_font.render(
        f"COLLISION RISK: {risk_state}",
        True,
        risk_colour
    )

    target_text = small_font.render(
        f"Target Speed: "
        f"{target_speed * 10:.0f} km/h",
        True,
        (180, 220, 255)
    )

    controls = small_font.render(
        "A = Toggle Autonomy   "
        "R = Reset",
        True,
        (220, 220, 220)
    )

    screen.blit(
        title,
        (20, 20)
    )

    screen.blit(
        telemetry,
        (20, 52)
    )

    screen.blit(
        mode,
        (20, 80)
    )

    screen.blit(
        distance_text,
        (20, 110)
    )

    screen.blit(
        target_text,
        (20, 137)
    )

    screen.blit(
        risk_text,
        (20, 165)
    )

    screen.blit(
        controls,
        (20, 195)
    )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
