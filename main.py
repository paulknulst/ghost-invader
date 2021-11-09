import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('back.png')

# # Sound
# mixer.music.load("background-music.wav")
# mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Ghost Invader")
icon = pygame.image.load('launch.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 12

# Some Const
ENEMY_START_Y = 64
SIZE_OF_ENEMY = 64
START_SPEED = 0.2


def create_enemy(counter):
    enemyImg.append(pygame.image.load('ghost.png'))
    enemyX.append(counter * (SIZE_OF_ENEMY + 1))
    enemyY.append(ENEMY_START_Y)
    enemyX_change.append(START_SPEED)
    enemyY_change.append(SIZE_OF_ENEMY + 5)


for i in range(num_of_enemies):
    create_enemy(i)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('laser.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.7
bullet_state = "ready"

# Score

score_value = 0
lifes = 3

font = pygame.font.Font('freesansbold.ttf', 32)

scoreTextX = 10
scoreTextY = 10

lifeTextX = 680
lifeTextY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def reset_enemy(conter):
    enemyX[conter] = 0
    enemyY[conter] = 64
    enemyX_change[conter] = START_SPEED
    enemyY_change[conter] = SIZE_OF_ENEMY + 5


def show_score(x, y):
    score_text = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score_text, (x, y))


def show_lifes(x, y):
    life_text = font.render("Life: " + str(lifes), True, (255, 0, 0))
    screen.blit(life_text, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            if lifes == 0:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break
            else:
                lifes -= 1
                reset_enemy(i)
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = START_SPEED
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -START_SPEED
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            reset_enemy(i)
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(scoreTextX, scoreTextY)
    show_lifes(lifeTextX, lifeTextY)
    pygame.display.update()
