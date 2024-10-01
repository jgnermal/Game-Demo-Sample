import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Race")

BG = pygame.transform.scale(pygame.image.load(".\images\Space.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5
ASTEROID_VEL = 10

ASTEROID_WIDTH = 10
ASTEROID_HEIGHT = 20

LASER_WIDTH = WIDTH
LASER_HEIGHT = 3

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, asteroids, lasers):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (WIDTH - 150, 10))

    pygame.draw.rect(WIN, "blue", player)   

    for asteroid in asteroids:
        pygame.draw.rect(WIN, "gray", asteroid)

    for laser in lasers:
        pygame.draw.rect(WIN, "red", laser)

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                        PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    asteroid_add_increment = 2000
    asteroid_count = 0

    laser_add_increment = 5000
    laser_count = 0
    laser_lifespan = 2000

    asteroids = []
    lasers =[]
    hit = False

    while run:
        asteroid_count += clock.tick(60)
        laser_count += clock.tick(60)

        elapsed_time = time.time() - start_time

        if asteroid_count > asteroid_add_increment:
            for _ in range(3):
                asteroid_x = random.randint(0, WIDTH - ASTEROID_WIDTH)
                asteroid = pygame.Rect(asteroid_x, -ASTEROID_HEIGHT, ASTEROID_WIDTH, ASTEROID_HEIGHT)
                asteroids.append(asteroid)

            asteroid_add_increment = max(200, asteroid_add_increment - 50)
            asteroid_count = 0

        if laser_count > laser_add_increment:
            for _ in range(2):
                laser_y = random.randint(0, HEIGHT - LASER_HEIGHT)
                laser = pygame.Rect(0, laser_y, LASER_WIDTH, LASER_HEIGHT)
                lasers.append(laser)

            laser_add_increment = max(500, laser_add_increment - 50)
            laser_count = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >=0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + PLAYER_HEIGHT <= HEIGHT:
            player.y += PLAYER_VEL

        for asteroid in asteroids[:]:
            asteroid.y += ASTEROID_VEL
            if asteroid.y > HEIGHT:
                asteroids.remove(asteroid)
            elif asteroid.y + asteroid.height >= player.y and asteroid.colliderect(player):
                asteroids.remove(asteroid)
                hit = True
                break 

        for laser in lasers[:]:
            if laser_lifespan < laser_count:
                lasers.remove(laser)

            elif laser.y + laser.height >= player.y and laser.colliderect(player):
                lasers.remove(laser)
                hit=True
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1 ,"white")
            WIN.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))    
            pygame.display.update()
            pygame.time.delay(3000)
            break

        draw(player, elapsed_time, asteroids, lasers)

    pygame.quit()

if __name__ == "__main__":
    main()