import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 800
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
WIN = pygame.display.set_mode([WIDTH, HEIGHT])

HEALTH_FONT = pygame.font.SysFont('comicsans', 40) 
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
WHITE = (200,200,200)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

FPS = 60

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3' ))
BULLTET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

VEL = 5
BULLET_VEL = 7
MAX_NUM_BULLET = 5

BORDER = pygame.Rect(590, 0, 20, HEIGHT)
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

pygame.display.set_caption("Minh's First Pygame!!!")

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BACKGROUND, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, ((WIDTH - red_health_text.get_width() - 10), 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)


    pygame.display.update()

def handle_yellow_movement(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x : # RIGHT
        yellow.x += VEL
    if key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: # DOWN
        yellow.y += VEL
    if key_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
        yellow.y -= VEL

def handle_red_movement(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # LEFT
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
        red.x += VEL
    if key_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: # DOWN
        red.y += VEL
    if key_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
        red.y -= VEL

def handle_bullet(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if bullet.colliderect(red):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if bullet.colliderect(yellow):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winnner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
            
def main():
    red = pygame.Rect(750, 325, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    yellow = pygame.Rect(250, 325, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    red_bullets = []
    yellow_bullets = []
    red_health, yellow_health = 10, 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v and len(yellow_bullets) < MAX_NUM_BULLET:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2, 5,5 )
                    yellow_bullets.append(bullet)
                    BULLTET_FIRE_SOUND.play()
                if event.key == pygame.K_m and len(red_bullets) < MAX_NUM_BULLET: 
                    bullet = pygame.Rect(red.x, red.y + red.height/2, 5,5 )
                    red_bullets.append(bullet)
                    BULLTET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        if winner_text != "":
            draw_winnner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        handle_yellow_movement(key_pressed, yellow)
        handle_red_movement(key_pressed, red)
        handle_bullet(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    
    main()


if __name__ == "__main__":
    main()