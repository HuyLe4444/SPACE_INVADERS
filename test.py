import pygame
import random
import os
pygame.font.init()

WIDTH, HEIGHT = 500, 700
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
SPACESHIP = pygame.transform.rotate(pygame.transform.scale(SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)
ENEMY_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
ENEMY = pygame.transform.scale(ENEMY_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'earth_at_night.png')), (WIDTH, HEIGHT))

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_ENEMY_BULLETS = 1

PLAYER_GET_HIT = pygame.USEREVENT + 1
SPAWN_ENEMY = pygame.USEREVENT + 2
ENEMY_SHOOT = pygame.USEREVENT + 3
PLAYER_GET_POINT = pygame.USEREVENT + 4
pygame.time.set_timer(SPAWN_ENEMY, 1000)
pygame.time.set_timer(ENEMY_SHOOT, 500)

LOSER_FONT = pygame.font.SysFont('comicsans', 100)
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
POINT_FONT = pygame.font.SysFont('comicsans', 20)


def draw_window(player, enemy, player_bullet, enemy_bullet, player_health, enemy_list, enemy_bullet_temp, player_point):
    WIN.blit(SPACE, (0, 0))
    WIN.blit(SPACESHIP, (player.x, player.y))
    WIN.blit(ENEMY, (enemy.x, enemy.y))
    
    player_health_text = HEALTH_FONT.render("Health: " + str(player_health), 1, WHITE)
    WIN.blit(player_health_text, (10, 10))
    player_point_text = POINT_FONT.render("Point: " + str(player_point), 1, WHITE)
    WIN.blit(player_point_text, (10, 30))
    
    for bullet in player_bullet:
        pygame.draw.rect(WIN, RED, bullet)
        for enemy_temp in enemy_list:
            if enemy_temp.colliderect(bullet):
                pygame.event.post(pygame.event.Event(PLAYER_GET_POINT))
                enemy_list.remove(enemy_temp)
                player_bullet.remove(bullet)
    for e_bullet in enemy_bullet:
        pygame.draw.rect(WIN, RED, e_bullet)
    for e_bullet in enemy_bullet_temp:
        e_bullet.y += BULLET_VEL
        if e_bullet.colliderect(player):
            pygame.event.post(pygame.event.Event(PLAYER_GET_HIT))
            enemy_bullet_temp.remove(e_bullet)
        elif e_bullet.y > HEIGHT:
            enemy_bullet_temp.remove(e_bullet)
        pygame.draw.rect(WIN, RED, e_bullet)
    for enemy_temp in enemy_list:
        enemy_temp.y += VEL
        if enemy_temp.colliderect(player):
            enemy_list.remove(enemy_temp)
            pygame.event.post(pygame.event.Event(PLAYER_GET_HIT))
        WIN.blit(ENEMY, (enemy_temp.x, enemy_temp.y))
            
        
    
    pygame.display.update()
    

def player_movement(key_pressed, player, enemy):
    if key_pressed[pygame.K_a] and player.x - VEL > 0:                           #LEFT
        player.x -= VEL
    if key_pressed[pygame.K_d] and player.x + VEL < WIDTH - SPACESHIP_WIDTH:     #RIGHT
        player.x += VEL
    if key_pressed[pygame.K_s] and player.y + VEL < HEIGHT - SPACESHIP_HEIGHT:   #DOWN
        player.y += VEL
    if key_pressed[pygame.K_w] and player.y - VEL > 0:                           #UP
        player.y -= VEL
        
    if player.colliderect(enemy):
        pygame.event.post(pygame.event.Event(PLAYER_GET_HIT))
        enemy_get_hit(enemy)
        
        
def player_handle_bullets(player_bullet, enemy):
    for bullet in player_bullet:
        bullet.y -= BULLET_VEL
        if bullet.y < 0:
            player_bullet.remove(bullet)
        elif enemy.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER_GET_POINT))
            enemy_get_hit(enemy)
            player_bullet.remove(bullet)
            
            
def enemy_shot(player, enemy_bullet):
    for e_bullet in enemy_bullet:
        e_bullet.y += BULLET_VEL
        if e_bullet.y > HEIGHT:
            enemy_bullet.remove(e_bullet)
        elif player.colliderect(e_bullet):
            pygame.event.post(pygame.event.Event(PLAYER_GET_HIT))
            enemy_bullet.remove(e_bullet)
                
                
def enemy_movement(enemy):
    enemy.y += VEL
                

def enemy_get_hit(enemy):
    enemy.x = -50
    enemy.y = -50
    

def draw_loser(out_of_health):
    draw_text = LOSER_FONT.render(out_of_health, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() // 2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    player = pygame.Rect(WIDTH//2 - SPACESHIP_WIDTH//2, HEIGHT - 100 , SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    enemy = pygame.Rect(WIDTH//2 - SPACESHIP_WIDTH//2, 100 , SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    player_bullet = []
    enemy_bullet = []
    enemy_list = []
    enemy_bullet_temp = []
    
    clock = pygame.time.Clock()
    
    player_health = 3
    player_point = 0
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    bullet = pygame.Rect(player.x + player.width//2 - 2, player.y, 5, 10)
                    player_bullet.append(bullet)
                    
            if event.type == PLAYER_GET_HIT:
                player_health -= 1
            
            if event.type == SPAWN_ENEMY:
                enemy_temp = pygame.Rect(random.randint(50, 450), 0, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
                enemy_list.append(enemy_temp)
                
            if event.type == ENEMY_SHOOT:
                e_bullet = pygame.Rect(enemy.x + enemy.width//2 - 2, enemy.y + enemy.height - 10, 5, 10)
                enemy_bullet.append(e_bullet)
                for enemy_temp in enemy_list:
                    e_bullet = pygame.Rect(enemy_temp.x + enemy_temp.width//2 - 2, enemy_temp.y + enemy_temp.height - 10, 5, 10)
                    enemy_bullet_temp.append(e_bullet)
                    
            if event.type == PLAYER_GET_POINT:
                player_point += 100
        
            
        out_of_health = ""
        if player_health <= 0:
            out_of_health = "NOOOOB!"
        if out_of_health != "":
            draw_loser(out_of_health)
                
        key_pressed = pygame.key.get_pressed()        
        
        enemy_shot(player, enemy_bullet)
        player_handle_bullets(player_bullet, enemy)
        player_movement(key_pressed, player, enemy)
        enemy_movement(enemy)
        draw_window(player, enemy, player_bullet, enemy_bullet, player_health, enemy_list, enemy_bullet_temp, player_point)
        
        pygame.display.update()

    main()
    
if __name__ == "__main__":
    main()
