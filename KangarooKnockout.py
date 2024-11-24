import pygame
import sys
import time
import random

# Character dictionaries
c1 = dict(
    name="you", health=100, punch=8, bamboo=0, jar=0, accuracy=10, speed=0.5, heal=0
)
c2 = dict(
    name="shadow", health=100, punch=5, bamboo=0, jar=0, accuracy=8, speed=0.5, heal=0
)
traits = ["spikes", "armor", "accuracy", "dodging", "fire", "regen", "bamboo", "speed"]
mytrait = []
# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Window with Tiles and Moving Kangaroos")

# Define tile size
TILE_WIDTH = SCREEN_WIDTH // 30
TILE_HEIGHT = SCREEN_HEIGHT // 20

# Colors
DARK_BLUE = (0, 0, 139)
DARK_GREEN = (34, 139, 34)
DARK_GRAY = (105, 105, 105)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


# Load kangaroo images
kangaroo_image_1 = pygame.image.load(
    f"pygame/Kangaroo_Knockout_Sprites/0-0kangaroo_og.png"
)
kangaroo_image_1 = pygame.transform.scale(
    kangaroo_image_1, (4 * TILE_WIDTH, 4 * TILE_HEIGHT)
)
kangaroo_image_2 = pygame.image.load(
    f"pygame/Kangaroo_Knockout_Sprites/1-0kangaroo_pp.png"
)
kangaroo_image_2 = pygame.transform.scale(
    kangaroo_image_2, (4 * TILE_WIDTH, 4 * TILE_HEIGHT)
)
font = pygame.font.SysFont(None, 36)


# Function to draw buttons
def draw_buttons(
    random_traits, button_x, button_y_start, button_width, button_height, button_y_gap
):
    for i, trait in enumerate(random_traits):
        button_y = button_y_start + i * (button_height + button_y_gap)
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, GREEN, button_rect)
        font = pygame.font.SysFont(None, 36)
        text = font.render(trait, True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)


# Function to check button clicks
def check_button_clicks(
    pos,
    random_traits,
    button_x,
    button_y_start,
    button_width,
    button_height,
    button_y_gap,
    selected_traits,
):
    for i, trait in enumerate(random_traits):
        button_y = button_y_start + i * (button_height + button_y_gap)
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        if button_rect.collidepoint(pos):
            if trait not in selected_traits:
                selected_traits.append(trait)
            if len(selected_traits) == 2:
                return True
    return False


def apply_traits(c1, c2, trait):
    if trait == "spikes":
        c1["punch"] *= 10
    elif trait == "armor":
        c1["health"] *= 1.5
    elif trait == "accuracy":
        c1["accuracy"] += 10
    elif trait == "dodging":
        c2["accuracy"] -= 5
    elif trait == "fire":
        c2["heal"] -= 3
    elif trait == "regen":
        c1["heal"] += 2
    elif trait == "bamboo":
        c1["bamboo"] += 10
    elif trait == "speed":
        c1["speed"] += 0.8


score = 0
oppscore = 0

# Main game loop
for n in range(5):
    c1["health"] = 100
    c2["health"] = 100

    # Reset kangaroo properties
    kangaroo_x = 0
    kangaroo_y = SCREEN_HEIGHT - 6 * TILE_HEIGHT
    kangaroo_speed = c1["speed"]

    blue_kangaroo_width = 4 * TILE_WIDTH
    blue_kangaroo_height = 4 * TILE_HEIGHT
    blue_kangaroo_x = SCREEN_WIDTH - blue_kangaroo_width
    blue_kangaroo_y = SCREEN_HEIGHT - 6 * TILE_HEIGHT
    blue_kangaroo_speed = c2["speed"]

    # Health bar properties
    health_bar_width = 10 * TILE_WIDTH
    health_bar_height = TILE_HEIGHT // 2
    health_bar_x = SCREEN_WIDTH // 2 - health_bar_width // 2
    health_bar_y = 10

    # Randomly select 5 traits for the buttons, excluding used traits
    if len(traits) > 4:
        random_traits = random.sample(traits, 5)
    else:
        random_traits = traits
    # list -> random_traits
    # loop through list

    # Button properties
    button_width = 200
    button_height = 50
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y_start = 100
    button_y_gap = 20

    # Selected traits
    selected_traits = []

    # Collision cooldown
    last_collision_time = 0
    collision_cooldown = 0.8

    start_screen = True
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False

            # if i == "spikes":

            if start_screen and event.type == pygame.MOUSEBUTTONDOWN:
                if check_button_clicks(
                    event.pos,
                    random_traits,
                    button_x,
                    button_y_start,
                    button_width,
                    button_height,
                    button_y_gap,
                    selected_traits,
                ):
                    x = random.randint(1, 2)
                    if x == 1:
                        apply_traits(c1, c2, selected_traits[0])
                        mytrait.append(selected_traits[0])
                        apply_traits(c2, c1, selected_traits[1])
                    if x == 2:
                        apply_traits(c2, c1, selected_traits[0])
                        apply_traits(c1, c2, selected_traits[1])
                        mytrait.append(selected_traits[1])
                    kangaroo_speed = c1["speed"]
                    blue_kangaroo_speed = c2["speed"]
                    start_screen = False
        if start_screen:
            screen.fill(DARK_BLUE)
            draw_buttons(
                random_traits,
                button_x,
                button_y_start,
                button_width,
                button_height,
                button_y_gap,
            )
            if n != 4:
                selected_traits_text = font.render(
                    f"Choose 2 traits, 1 will be yours, the other your shadows",
                    True,
                    WHITE,
                )
                screen.blit(selected_traits_text, (100, 500))

        else:
            # Move the kangaroo towards the right
            kangaroo_x += kangaroo_speed

            # Move the blue kangaroo towards the left
            blue_kangaroo_x -= blue_kangaroo_speed

            # Ensure the kangaroos stay within the screen boundaries
            if kangaroo_x < 0:
                kangaroo_x = 0
            if kangaroo_x > SCREEN_WIDTH - blue_kangaroo_width:
                kangaroo_x = SCREEN_WIDTH - blue_kangaroo_width

            if blue_kangaroo_x < 0:
                blue_kangaroo_x = 0
            if blue_kangaroo_x > SCREEN_WIDTH - blue_kangaroo_width:
                blue_kangaroo_x = SCREEN_WIDTH - blue_kangaroo_width

            distancebetween = abs(kangaroo_x - blue_kangaroo_x) / TILE_WIDTH
            if distancebetween <= 7:
                if c1["bamboo"] != 0:
                    kangaroo_speed = 0

                elif c2["bamboo"] != 0:
                    blue_kangaroo_speed = 0

            if distancebetween <= 3:
                kangaroo_speed = 0
                blue_kangaroo_speed = 0

            # Check if the kangaroos are three tiles apart
            current_time = time.time()
            kangaroo_rect = pygame.Rect(
                kangaroo_x, kangaroo_y, blue_kangaroo_width, blue_kangaroo_height
            )
            blue_kangaroo_rect = pygame.Rect(
                blue_kangaroo_x,
                blue_kangaroo_y,
                blue_kangaroo_width,
                blue_kangaroo_height,
            )
            if (
                distancebetween <= 7
                and current_time - last_collision_time >= collision_cooldown
            ):
                last_collision_time = current_time

                if c1["bamboo"] != 0:
                    kangaroo_speed = 0
                    if distancebetween > 6:
                        y = random.randint(1, 10)
                        if c1["accuracy"] >= y:
                            c2["health"] -= c1["bamboo"]
                    else:
                        blue_kangaroo_speed = 0
                        y = random.randint(1, 10)
                        if c2["accuracy"] >= y:
                            c1["health"] -= c2["punch"]
                        x = random.randint(1, 10)
                        if c1["accuracy"] >= x:
                            c2["health"] -= c1["punch"]
                elif c2["bamboo"] != 0:
                    blue_kangaroo_speed = 0
                    if distancebetween > 3:
                        y = random.randint(1, 10)
                        if c2["accuracy"] >= y:
                            c1["health"] -= c2["bamboo"]
                    else:
                        kangaroo_speed = 0
                        y = random.randint(1, 10)
                        if c2["accuracy"] >= y:
                            c1["health"] -= c2["punch"]
                        x = random.randint(1, 10)
                        if c1["accuracy"] >= x:
                            c2["health"] -= c1["punch"]
                else:
                    if distancebetween <= 4:
                        kangaroo_speed = 0
                        blue_kangaroo_speed = 0
                        x = random.randint(1, 10)
                        if c2["accuracy"] >= x:
                            c1["health"] -= c2["punch"]
                        y = random.randint(1, 10)
                        if c1["accuracy"] >= y:
                            c2["health"] -= c1["punch"]
                c1["health"] += c1["heal"]
                c2["health"] += c2["heal"]
                print(c1["health"])
                print(c2["health"])
                if c1["health"] <= 0:
                    c1["health"] = 0
                    oppscore += 1
                    running = False
                if c2["health"] <= 0:
                    c2["health"] = 0
                    score += 1
                    running = False

                if c1["health"] <= 0 and c2["health"] <= 0:
                    if c1 < c2:
                        oppscore += 1
                    else:
                        score += 1
                    running = False

            # Fill the screen with a dark blue color for the sky
            screen.fill(DARK_BLUE)

            # Draw the tiles
            for row in range(20):
                for col in range(30):
                    tile_rect = pygame.Rect(
                        col * TILE_WIDTH, row * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT
                    )
                    if row >= 18:
                        pygame.draw.rect(screen, DARK_GREEN, tile_rect)
                    else:
                        pygame.draw.rect(screen, DARK_BLUE, tile_rect)
                    pygame.draw.rect(screen, DARK_GRAY, tile_rect, 1)

            # Draw the moving kangaroos
            screen.blit(kangaroo_image_1, (kangaroo_x, kangaroo_y))
            screen.blit(kangaroo_image_2, (blue_kangaroo_x, blue_kangaroo_y))

            # Draw the health bars
            for i in range(round(c1["health"] // 10)):
                health_tile_rect = pygame.Rect(
                    health_bar_x + i * TILE_WIDTH,
                    health_bar_y,
                    TILE_WIDTH,
                    health_bar_height,
                )
                pygame.draw.rect(screen, RED, health_tile_rect)
            for i in range(round(c2["health"] // 10)):
                health_tile_rect = pygame.Rect(
                    health_bar_x + i * TILE_WIDTH,
                    health_bar_y + TILE_HEIGHT,
                    TILE_WIDTH,
                    health_bar_height,
                )
                pygame.draw.rect(screen, BLUE, health_tile_rect)

            #  coordinates of the objects
            kangaroo_coords = font.render(
                f"Kangaroo: ({kangaroo_x}, {kangaroo_y})", True, WHITE
            )
            blue_kangaroo_coords = font.render(
                f"Blue Kangaroo: ({blue_kangaroo_x}, {blue_kangaroo_y})", True, WHITE
            )

            # Display selected traits
            selected_traits_text = font.render(
                f'Selected Traits: {", ".join(mytrait)}', True, WHITE
            )
            screen.blit(selected_traits_text, (10, 200))
            selected_traits_text = font.render(
                f"Your Health: {str (c1['health'])}", True, WHITE
            )
            screen.blit(selected_traits_text, (10, 10))
            selected_traits_text = font.render(
                f"Opp Health: {str (c2['health'])}", True, WHITE
            )
            screen.blit(selected_traits_text, (10, 40))

        # Update the display
        pygame.display.flip()

    # Remember to removeAdd  traits
    traits.remove(selected_traits[0])
    traits.remove(selected_traits[1])
    selected_traits.clear()
        if n == 4:
        if oppscore > score:
            selected_traits_text = font.render(f"YOU WIN", True, WHITE)
            screen.blit(selected_traits_text, (100, 500))
        else:
            selected_traits_text = font.render(f"YOU LOSE", True, WHITE)
            screen.blit(selected_traits_text, (100, 500))

    pygame.display.flip()
pygame.quit()
sys.exit()
