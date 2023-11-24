import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
player_size = 50
player_speed = 5
collectible_size = 20
obstacle_size = 30
enemy_size = 40
background_speed = 2

START_MENU = 0
PLAYING = 1
LEVEL_COMPLETED = 2
GAME_OVER = 9

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PythonProject")

font = pygame.font.Font(None, 36)

def draw_player(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, player_size, player_size))

def draw_collectible(x, y):
    pygame.draw.circle(screen, (255, 255, 0), (x, y), collectible_size)

def draw_obstacle(x, y, size):
    pygame.draw.rect(screen, (128, 128, 128), (x, y, size, size))

def draw_enemy(x, y):
    pygame.draw.rect(screen, (255, 0, 0), (x, y, enemy_size, enemy_size))

def draw_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

def start_menu():
    show_menu = True
    while show_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                show_menu = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_h]:
            how_to_play()

        screen.fill(BLACK)
        draw_text("Cube Game", WIDTH // 2 - 100, HEIGHT // 2 - 50)
        draw_text("Press SPACE to start", WIDTH // 2 - 150, HEIGHT // 2 + 50)
        draw_text("Press 'H' for How to Play", WIDTH // 2 - 180, HEIGHT // 2 + 100)
        pygame.display.flip()

        pygame.time.Clock().tick(FPS)

def check_password():
    password_input = input("Enter the password: ")
    return password_input == admin_password

def how_to_play():
    screen.fill(BLACK)
    draw_text("How to Play", WIDTH // 2 - 100, HEIGHT // 4)
    instructions = [
        "Use arrow keys to move the player.",
        "Collect yellow coins to increase your score.",
        "Collect enough coins to gain a bonus life.",
        "Avoid obstacles and red enemies.",
        "Running out of health or time ends the level.",
        "Complete each level to progress.",
        "On Level 10, you face a challenging maze.",
        "Good luck and have fun!",
    ]
    y_offset = HEIGHT // 4 + 50
    for instruction in instructions:
        draw_text(instruction, WIDTH // 2 - 200, y_offset)
        y_offset += 40
    draw_text("Press SPACE to go back", WIDTH // 2 - 200, HEIGHT - 100)
    pygame.display.flip()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting_for_key = False


def game_over(score):
    screen.fill(BLACK)
    draw_text(f"Game Over! Your Score: {score}", WIDTH // 2 - 200, HEIGHT // 2 - 50)
    draw_text("Press SPACE to play again", WIDTH // 2 - 200, HEIGHT // 2 + 50)
    pygame.display.flip()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting_for_key = False

game_state = START_MENU
invincible = False 

level_timer = 0
pgdn_pressed = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                if check_password():
                    invincible = not invincible

            if event.key == pygame.K_PAGEDOWN:
               
                pgdn_pressed += 1
               
                if pgdn_pressed == 2:
                    level_timer = 0  

    if game_state == START_MENU:
        start_menu()
        game_state = PLAYING

    if game_state == PLAYING:
        score = 0
        health = 3
        level = 1

        level_timer = max(30, 30 + 3 * (level - 1)) 

        while (health > 0 and level_timer > 0) or health > 0:
            
            x, y = WIDTH // 2 - player_size // 2, HEIGHT // 2 - player_size // 2

            
            x, y = WIDTH // 2 - player_size // 2, HEIGHT // 2 - player_size // 2

            if level == 10:
                
                x, y = 50, 50

            
            collectibles = []
            obstacles = []
            enemies = []

            if level == 10:
                
                obstacles.append((0, 0, WIDTH, 10))  
                obstacles.append((0, 0, 10, HEIGHT))  
                obstacles.append((WIDTH - 10, 0, 10, HEIGHT))  
                obstacles.append((0, HEIGHT - 10, WIDTH, 10))  
                obstacles.append((100, 100, 200, 10))  
                enemies.extend([(100, 200), (150, 200), (200, 200), (250, 200), (300, 200)])  
                collectibles.extend([(100, 300), (150, 300), (200, 300), (250, 300), (300, 300)])  

            while len(collectibles) < int(5 * 1.2 ** level):
                
                collectible_position = (random.randint(0, WIDTH - collectible_size), random.randint(0, HEIGHT - collectible_size))

                
                if all(
                    pygame.Rect(collectible_position, (collectible_size, collectible_size)).colliderect(pygame.Rect(enemy_position, (enemy_size, enemy_size))) is False
                    for enemy_position in enemies
                ):
                    collectibles.append(collectible_position)

            
            while len(enemies) < int(5 * 1.1 ** level):
                enemy_position = (random.randint(0, WIDTH - enemy_size), random.randint(0, HEIGHT - enemy_size))

                
                if all(
                    not pygame.Rect(enemy_position, (enemy_size, enemy_size)).colliderect(pygame.Rect(e[0], e[1], enemy_size, enemy_size))
                    for e in enemies
                ) and all(
                     not pygame.Rect(enemy_position, (enemy_size, enemy_size)).colliderect(pygame.Rect(c[0], c[1], collectible_size, collectible_size))
                    for c in collectibles
                ):
                    enemies.append(enemy_position)

            obstacles.extend([(random.randint(0, WIDTH - obstacle_size), random.randint(0, HEIGHT - obstacle_size), obstacle_size) for _ in range(int(5 * level))])

            
            bg_x = 0
            bg_width = WIDTH * 2
            bg_color = (70, 70, 70)

            
            level_timer = max(30, 30 + 3 * (level - 1))  

            
            coin_requirement = 5 * level

            
            while (health > 0 and level_timer > 0) or health > 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT] and x > 0:
                    x -= player_speed
                if keys[pygame.K_RIGHT] and x < WIDTH - player_size:
                    x += player_speed
                if keys[pygame.K_UP] and y > 0:
                    y -= player_speed
                if keys[pygame.K_DOWN] and y < HEIGHT - player_size:
                    y += player_speed

                
                bg_x -= background_speed
                if bg_x < -bg_width:
                    bg_x = 0

                if not invincible:
                    for collectible in collectibles[:]:
                        if (
                            collectible[0] < x + player_size
                            and collectible[0] + collectible_size > x
                            and collectible[1] < y + player_size
                            and collectible[1] + collectible_size > y
                        ):
                            collectibles.remove(collectible)
                            score += 1
                            
                            if not collectibles:
                                level_timer -= 100  
                                
                                if score >= coin_requirement:
                                    health += 1  
                                    score += 10  
                                else:
                                    health -= 1  
                                break

                
                for obstacle in obstacles:
                    if (
                        obstacle[0] < x + player_size
                        and obstacle[0] + obstacle[2] > x
                        and obstacle[1] < y + player_size
                        and obstacle[1] + obstacle[2] > y
                    ):
                        obstacles.remove(obstacle)
                        health -= 1

                
                for enemy in enemies[:]:
                    if (
                        enemy[0] < x + player_size
                        and enemy[0] + enemy_size > x
                        and enemy[1] < y + player_size
                        and enemy[1] + enemy_size > y
                    ):
                        enemies.remove(enemy)
                        health -= 1

                screen.fill(bg_color)
                pygame.draw.rect(screen, bg_color, (bg_x, 0, bg_width, HEIGHT))

                
                for collectible in collectibles:
                    draw_collectible(*collectible)

                
                for obstacle in obstacles:
                    draw_obstacle(*obstacle)

                
                for enemy in enemies:
                    draw_enemy(*enemy)

                
                draw_player(x, y)

                
                draw_text(f"Score: {score}", 10, 10)
                draw_text(f"Health: {health}", WIDTH - 150, 10)
                draw_text(f"Time: {int(level_timer)}", WIDTH // 2 - 50, 10)

                
                pygame.display.flip()

                
                pygame.time.Clock().tick(FPS)

                
                level_timer -= 1 / FPS

                
                if level_timer <= 0:
                    break

            
            if level <= 10:
                screen.fill(BLACK)
                draw_text(f"Level {level} completed!", WIDTH // 2 - 150, HEIGHT // 2 - 50)
                pygame.display.flip()
                pygame.time.delay(2000)  
                level += 1
                game_state = PLAYING

        if health <= 0 or level > 10:
            game_over(score)
            game_state = START_MENU
            level = 1
            game_over(score)
            game_state = START_MENU
            level = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        game_state = START_MENU

    screen.fill(BLACK)
    draw_text("Thanks for playing!", WIDTH // 2 - 150, HEIGHT // 2 - 50)
    draw_text(f"Final Score: {score}", WIDTH // 2 - 150, HEIGHT // 2 + 50)
    draw_text("Press SPACE to play again", WIDTH // 2 - 180, HEIGHT // 2 + 100)
    pygame.display.flip()

    pygame.time.Clock().tick(FPS)
