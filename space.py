import pygame
import random
import sys
import math

pygame.init()

playerx = 380
playery = 530
bullety = 500
bullet_shot = False
bullet_initial_x = playerx
euyx = [430, 544, 700, 234, 699, 69, 420]
eyx = [457, 263, 293, 549, 398, 438, 234, 194, 346, 700]
enemyx = random.choice(euyx)
enemyy = -100
enemyq = random.choice(eyx)
enemyyy = -200
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
GOLD = (255, 215, 0)
GREY = (106, 105, 105)
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)
score = 0
game_over_displayed = False
selected_spaceship_color = CYAN  
spaceship_colors = [CYAN, (255, 0, 0), (0, 255, 0), (255, 255, 0)] 
spaceship_index = 0 
level = 0
show_main_menu = True
show_spaceship_selection = False
show_rules = False
is_paused = False

# Functions
def draw_triangle(screen, x, y, color):
    points = [(x, y), (x - 20, y + 40), (x + 20, y + 40)]
    pygame.draw.polygon(screen, color, points)

def draw_hexagon(screen, x, y):
    hex_points = []
    for i in range(6):
        angle = math.radians(60 * i)
        point_x = x + 20 * math.cos(angle)
        point_y = y + 20 * math.sin(angle)
        hex_points.append((point_x, point_y))
    pygame.draw.polygon(screen, GREEN, hex_points, 5)
    pygame.draw.polygon(screen, BLACK, hex_points)

def draw_bullet(screen, x, y):
    pygame.draw.rect(screen, GOLD, (x, y, 5, 10))

def display_game_over(screen):
    game_over_text = font.render("GAME OVER", True, GREY)
    screen.blit(game_over_text, (250, 250))

def display_score(screen, score, level):
    score_text = small_font.render(f"Score: {score} | Level: {level}", True, CYAN)
    screen.blit(score_text, (10, 0))

def display_menu(screen):
    screen.fill(BLACK)
    title_text = font.render("Space Invaders", True, CYAN)
    start_text = small_font.render("1. Start Game", True, GOLD)
    spaceship_text = small_font.render("2. Change Spaceship", True, GREEN)
    rules_text = small_font.render("3. Rules", True, GREY)
    screen.blit(title_text, (250, 150))
    screen.blit(start_text, (250, 250))
    screen.blit(spaceship_text, (250, 300))
    screen.blit(rules_text, (250, 350))

def display_rules(screen):
    screen.fill(BLACK)
    rules_text = font.render("Game Rules", True, GREY)
    rule1 = small_font.render("1. Use 'A' and 'D' to move", True, GREY)
    rule2 = small_font.render("2. Press 'E' to shoot", True, GREY)
    rule3 = small_font.render("3. Score increases with each hit", True, GREY)
    rule4 = small_font.render("4. Don't let enemies pass the screen!", True, GREY)
    rule5 = small_font.render("5. Press 'P' to slow down the game", True, GREY)  
    back_text = small_font.render("Press 'B' to go back", True, GREY)
    screen.blit(rules_text, (250, 100))
    screen.blit(rule1, (100, 200))
    screen.blit(rule2, (100, 250))
    screen.blit(rule3, (100, 300))
    screen.blit(rule4, (100, 350))
    screen.blit(rule5, (100, 400))  
    screen.blit(back_text, (250, 450))

def spaceship_selection(screen):
    screen.fill(BLACK)
    select_text = small_font.render("Select Your Spaceship Color", True, CYAN)
    color_text = small_font.render("Use Left/Right Arrows to Change Color and B to confirm", True, GREEN)
    current_color_text = small_font.render(f"Current Color: {spaceship_colors[spaceship_index]}", True, spaceship_colors[spaceship_index])
    screen.blit(select_text, (270, 150))
    screen.blit(color_text, (100, 250))
    screen.blit(current_color_text, (190, 350))
    draw_triangle(screen, 400, 450, spaceship_colors[spaceship_index])

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_p]:
        is_paused = not is_paused

    if show_main_menu:
        display_menu(screen)
        if keys[pygame.K_1]:
            show_main_menu = False
        elif keys[pygame.K_2]:
            show_main_menu = False
            show_spaceship_selection = True
        elif keys[pygame.K_3]:
            show_main_menu = False
            show_rules = True
    elif show_spaceship_selection:
        spaceship_selection(screen)    
        if keys[pygame.K_RIGHT]:
            spaceship_index = (spaceship_index + 1) % len(spaceship_colors)
            selected_spaceship_color = spaceship_colors[spaceship_index]
        elif keys[pygame.K_LEFT]:
            spaceship_index = (spaceship_index - 1) % len(spaceship_colors)
            selected_spaceship_color = spaceship_colors[spaceship_index]
        elif keys[pygame.K_b]:
            show_spaceship_selection = False
            show_main_menu = True

    elif show_rules:
        display_rules(screen)
        if keys[pygame.K_b]:
            show_rules = False
            show_main_menu = True
    else:
        if not is_paused: 
            playerx += (keys[pygame.K_d] - keys[pygame.K_a]) * 2
            if keys[pygame.K_e] and not bullet_shot:
                bullet_shot = True
                bullety = playery
                bullet_initial_x = playerx

            if bullet_shot:
                bullety -= 5
                if bullety < 0:
                    bullet_shot = False

            if playerx <= 0:
                playerx = 0
            if playerx >= 755:
                playerx = 755

            enemyy += 0.5
            if enemyy >= 600:
                game_over_displayed = True
            enemyyy += 0.5
            if enemyy >= 600:
                enemyx = random.choice(euyx)
                enemyy = -100

            if enemyyy >= 600:
                enemyq = random.choice(eyx)
                enemyyy = -200

            player_rect = pygame.Rect(playerx - 20, playery, 40, 40)
            enemy_rect = pygame.Rect(enemyx - 20, enemyy - 20, 40, 40)
            enemy1_rect = pygame.Rect(enemyq - 20, enemyyy - 20, 40, 40)
            bullet_rect = pygame.Rect(bullet_initial_x, bullety, 5, 10)

            if bullet_shot and bullet_rect.colliderect(enemy_rect):
                enemyx = random.choice(euyx)
                enemyy = -100
                bullet_shot = False
                score += 10
            if bullet_shot and bullet_rect.colliderect(enemy1_rect):
                enemyq = random.choice(eyx)
                enemyyy = -150
                bullet_shot = False
                score += 10

            if score >= 60:
                level = 2
                enemyy += 1
                enemyyy += 1
            if score >= 120:
                level = 3
                enemyy += 1.5
                enemyyy += 1.5
            if score >= 190:
                level = 4
                enemyy += 2
                enemyyy += 2

            screen.fill(BLACK)
            if game_over_displayed:
                display_game_over(screen)
            else:
                draw_hexagon(screen, enemyx, enemyy)
                draw_hexagon(screen, enemyq, enemyyy)
                draw_triangle(screen, playerx, playery, selected_spaceship_color)
                if bullet_shot:
                    draw_bullet(screen, bullet_initial_x, bullety)
                display_score(screen, score, level)

    pygame.display.flip()
    clock.tick(200)

pygame.quit()
sys.exit()
