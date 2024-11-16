import pygame
import random
import sys
import time

# Initialise Pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pixel Rush")

# Colors and Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)  # Star color
font = pygame.font.Font(None, 36)

# Game variables
player_pos = [400, 300]
player_size = 50
player_speed = 5
score = 0
game_active = False
paused = False
enemy_spawn_time = 0  # Timer to track when to spawn enemies
enemy_spawn_interval = 7000  # Set interval to 7 seconds (7000 milliseconds)
enemy_speed = 1  # Speed of enemies

# Timers
star_timer = 0  # Timer for the star
star_interval = 30000  # 30 seconds (30000 milliseconds)

# Colored block and enemy settings
colored_blocks_size = 30
colored_blocks = []
enemies = []
power_ups = []
power_up_size = 30

# Star settings
star_size = 40
star_pos = None  # Position of the star
star_glow_direction = 1  # Controls pulsing animation (1 = growing, -1 = shrinking)
star_glow_size = star_size

# Function to spawn a star
def spawn_star():
    global star_pos
    x = random.randint(0, screen_width - star_size)
    y = random.randint(0, screen_height - star_size)
    star_pos = [x, y]

# Function to check for star collection
def collect_star():
    global score, star_pos
    if star_pos:
        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
        star_rect = pygame.Rect(star_pos[0], star_pos[1], star_glow_size, star_glow_size)
        if player_rect.colliderect(star_rect):
            score += 50
            star_pos = None  # Remove the star after collection

# Function to spawn colored blocks
def spawn_colored_block():
    x, y = random.randint(0, screen_width - colored_blocks_size), random.randint(0, screen_height - colored_blocks_size)
    color = random.choice([BLUE, GREEN, YELLOW])  # Randomly choose one of the colors
    colored_blocks.append({"pos": [x, y], "color": color})

# Function to spawn enemies
def spawn_enemy():
    x, y = random.randint(0, screen_width - player_size), random.randint(0, screen_height - player_size)
    direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])  # Random direction for enemy
    enemies.append({"pos": [x, y], "direction": direction, "speed": enemy_speed})

# Function to spawn power-ups
def spawn_power_up():
    x, y = random.randint(0, screen_width - power_up_size), random.randint(0, screen_height - power_up_size)
    type_of_power_up = random.choice(['SPEED', 'SHIELD', 'SCORE_MULTIPLIER'])
    power_ups.append({"pos": [x, y], "type": type_of_power_up})

# Function to move the enemies slowly
def move_enemies():
    for enemy in enemies:
        if enemy["direction"] == "UP":
            enemy["pos"][1] -= enemy["speed"]
        elif enemy["direction"] == "DOWN":
            enemy["pos"][1] += enemy["speed"]
        elif enemy["direction"] == "LEFT":
            enemy["pos"][0] -= enemy["speed"]
        elif enemy["direction"] == "RIGHT":
            enemy["pos"][0] += enemy["speed"]

        # Ensure enemies stay within bounds
        if enemy["pos"][0] < 0:
            enemy["pos"][0] = 0
            enemy["direction"] = random.choice(["RIGHT", "LEFT"])
        elif enemy["pos"][0] > screen_width - player_size:
            enemy["pos"][0] = screen_width - player_size
            enemy["direction"] = random.choice(["LEFT", "RIGHT"])
        if enemy["pos"][1] < 0:
            enemy["pos"][1] = 0
            enemy["direction"] = random.choice(["UP", "DOWN"])
        elif enemy["pos"][1] > screen_height - player_size:
            enemy["pos"][1] = screen_height - player_size
            enemy["direction"] = random.choice(["UP", "DOWN"])

# Function to check for collisions with colored blocks
def collect_colored_block():
    global score
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)

    for block in colored_blocks[:]:
        block_rect = pygame.Rect(block["pos"][0], block["pos"][1], colored_blocks_size, colored_blocks_size)
        if player_rect.colliderect(block_rect):
            score += 10  # Increase score when collecting a block
            colored_blocks.remove(block)  # Remove the collected block

# Function to check collisions with enemies
def check_for_enemy_collision():
    global game_active
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)

    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy["pos"][0], enemy["pos"][1], player_size, player_size)
        if player_rect.colliderect(enemy_rect):
            game_active = False  # End the game if player hits an enemy
            break

# Function to check collisions with power-ups
def collect_power_up():
    global player_speed, score
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)

    for power_up in power_ups[:]:
        power_up_rect = pygame.Rect(power_up["pos"][0], power_up["pos"][1], power_up_size, power_up_size)
        if player_rect.colliderect(power_up_rect):
            if power_up["type"] == "SPEED":
                player_speed += 2  # Increase player speed
            elif power_up["type"] == "SHIELD":
                # Implement shield logic (e.g., prevent damage from one enemy hit)
                pass
            elif power_up["type"] == "SCORE_MULTIPLIER":
                score += 20  # Temporary score multiplier boost
            power_ups.remove(power_up)

# Function to display a countdown before game starts
def display_countdown():
    countdown_font = pygame.font.Font(None, 100)
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        text = countdown_font.render(str(i), True, WHITE)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)
    screen.fill(BLACK)
    go_text = countdown_font.render("GO!", True, WHITE)
    screen.blit(go_text, (screen_width // 2 - go_text.get_width() // 2, screen_height // 2 - go_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)

# Function to display the score with a background
def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_bg = pygame.Surface((score_text.get_width() + 10, score_text.get_height() + 10))
    score_bg.fill(BLACK)
    screen.blit(score_bg, (10, 10))
    screen.blit(score_text, (15, 15))

# Function to animate the star glow
def animate_star_glow():
    global star_glow_size, star_glow_direction
    if star_pos:
        # Update the size for the pulsing effect
        star_glow_size += star_glow_direction
        if star_glow_size > star_size + 10 or star_glow_size < star_size - 10:
            star_glow_direction *= -1  # Reverse direction

# Main game loop
def game_loop():
    global game_active, score, paused, enemy_spawn_time, enemy_spawn_interval, player_pos, star_timer, star_pos
    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)

        if not game_active:
            # Display the instructions screen
            title_text = font.render("Welcome to Pixel Rush!", True, WHITE)
            instructions = [
                "Instructions:",
                "1. Use the arrow keys to move.",
                "2. Collect colored blocks to gain points.",
                "3. Avoid enemies - they will end the game if you collide with them!",
                "4. Collect power-ups to gain speed or score boosts.",
                "5. Collect the star for a big score bonus!",
                "6. Press SPACE to start the game."
            ]
            screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))

            # Draw instructions
            for i, line in enumerate(instructions            ):
                text = font.render(line, True, WHITE)
                screen.blit(text, (screen_width // 2 - text.get_width() // 2, 150 + i * 40))

            pygame.display.flip()

            # Wait for the user to press SPACE to start
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    player_pos[0], player_pos[1] = screen_width // 2, screen_height // 2
                    score = 0
                    colored_blocks.clear()
                    enemies.clear()
                    power_ups.clear()
                    enemy_spawn_time = pygame.time.get_ticks()  # Reset spawn timer
                    star_timer = pygame.time.get_ticks()  # Reset star timer
                    star_pos = None
                    display_countdown()  # Display countdown before game starts
            continue

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]:
            player_pos[1] += player_speed

        # Keep the player within the screen bounds
        player_pos[0] = max(0, min(player_pos[0], screen_width - player_size))
        player_pos[1] = max(0, min(player_pos[1], screen_height - player_size))

        # Spawn new colored blocks randomly
        if random.randint(1, 100) < 2:
            spawn_colored_block()

        # Spawn power-ups randomly
        if random.randint(1, 100) < 2:
            spawn_power_up()

        # Gradually spawn enemies after 7 seconds, ensuring not more than 15 enemies on screen
        current_time = pygame.time.get_ticks()
        if current_time - enemy_spawn_time > enemy_spawn_interval and len(enemies) < 15:
            spawn_enemy()  # Spawn an enemy
            enemy_spawn_time = current_time  # Reset the timer

        # Spawn a star every 30 seconds
        if current_time - star_timer > star_interval:
            spawn_star()
            star_timer = current_time  # Reset the star timer

        # Move enemies
        move_enemies()

        # Check for collisions with colored blocks
        collect_colored_block()

        # Check for collisions with enemies
        check_for_enemy_collision()

        # Check for collisions with power-ups
        collect_power_up()

        # Check for collisions with the star
        collect_star()

        # Animate the star glow
        animate_star_glow()

        # Draw the player (as a white rectangle)
        pygame.draw.rect(screen, WHITE, (player_pos[0], player_pos[1], player_size, player_size))

        # Draw the colored blocks (blue, green, yellow)
        for block in colored_blocks:
            pygame.draw.rect(screen, block["color"], (block["pos"][0], block["pos"][1], colored_blocks_size, colored_blocks_size))

        # Draw the enemies (red)
        for enemy in enemies:
            pygame.draw.rect(screen, RED, (enemy["pos"][0], enemy["pos"][1], player_size, player_size))

        # Draw the power-ups (yellow, green, blue)
        for power_up in power_ups:
            if power_up["type"] == 'SPEED':
                pygame.draw.rect(screen, YELLOW, (power_up["pos"][0], power_up["pos"][1], power_up_size, power_up_size))
            elif power_up["type"] == 'SHIELD':
                pygame.draw.rect(screen, GREEN, (power_up["pos"][0], power_up["pos"][1], power_up_size, power_up_size))
            elif power_up["type"] == 'SCORE_MULTIPLIER':
                pygame.draw.rect(screen, BLUE, (power_up["pos"][0], power_up["pos"][1], power_up_size, power_up_size))

        # Draw the star (gold) if it exists
        if star_pos:
            pygame.draw.ellipse(
                screen,
                GOLD,
                (star_pos[0] - (star_glow_size - star_size) // 2, 
                 star_pos[1] - (star_glow_size - star_size) // 2, 
                 star_glow_size, 
                 star_glow_size)
            )

        # Display the score
        display_score()

        pygame.display.flip()
        clock.tick(30)  # 30 FPS

# Run the game
game_loop()

