import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((900, 600))

# background
background = pygame.image.load('new space background.jpg')

# background music
mixer.music.load('background.wav')
mixer.music.play(-1)
# Title and icons
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo-flying (1).png')
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load('space-invaders.png')
playerX = 435
playerY = 480
playerX_change = 0
# playerY_change = 0

# enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)



# bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = "Ready"

#score
score_value = 0;
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 0, 0))
    screen.blit(over_text, (300, 270))

def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bullet_img,(x+16,y+10))

def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

# Game-loop
running = True
while running:
        screen.fill((255, 255, 255))
        # background image
        screen.blit(background, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if keystroke is pressed check whether its  left or right
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.3
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.3
                # if event.key == pygame.K_UP:
                #     playerY_change = -0.3
                # if event.key == pygame.K_DOWN:
                #     playerY_change = 0.3

                if event.key == pygame.K_SPACE:
                    if bullet_state is "Ready":
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    playerX_change = 0
                    playerY_change = 0

        playerX += playerX_change
        # playerY += playerY_change
        # setting boundaries
        if playerX <= 0:
            playerX = 0
        elif playerX >= 836:
            playerX = 836
        elif playerY <= 0:
            playerY = 0
        elif playerY >= 536:
            playerY = 536


        # Enemy movements
        for i in range(num_of_enemies):

            # Game over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 836:
                enemyX_change[i] = -0.2
                enemyY[i] += enemyY_change[i]

        # collision
            collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = "Ready"
                score_value += 1
                print(score_value)
                enemyX[i] = random.randint(0, 835)
                enemyY[i] = random.randint(50, 150)
            enemy(enemyX[i], enemyY[i], i)


        # bullet movements
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "Ready"

        if bullet_state is "Fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change



    # function calling
        player(playerX, playerY)
        show_score(textX, textY)
        pygame.display.update()
