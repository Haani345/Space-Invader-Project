import pygame
import math
import random

Screen_Width = 800
Screen_Height = 500
Player_Start_X = 370
Player_Start_Y = 380
Enemy_Start_Y_Min = 50
Enemy_Start_Y_Max = 150
Enemy_Speed_X = 5
Enemy_Speed_Y = 40
Bullet_Speed_Y = 10
Collision_Distance = 25

pygame.init()

Screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption('Space Invader')
Background = pygame.image.load('Background.jpg')

Player_image = pygame.image.load('player.png')
PlayerX = Player_Start_X
PlayerY = Player_Start_Y
Player_X_Change = 0

Enemy_image = []
Enemy_X = []
Enemy_Y = []
Enemy_X_Change = []
Enemy_Y_Change = []
Number_of_Enemies = 7

for i in range(Number_of_Enemies):
    Enemy_image.append(pygame.image.load('enemy.jpg'))
    Enemy_X.append(random.randint(0, Screen_Width - 64))
    Enemy_Y.append(random.randint(Enemy_Start_Y_Min, Enemy_Start_Y_Max))
    Enemy_X_Change.append(Enemy_Speed_X)
    Enemy_Y_Change.append(Enemy_Speed_Y)

Bullet_image = pygame.image.load('bullet.jpg')
Bullet_X = 0
Bullet_Y = Player_Start_Y
Bullet_Y_Change = Bullet_Speed_Y
Bullet_State = 'ready'

Score_Value = 0
Font = pygame.font.Font('freesansbold.ttf', 32)
Text_X = 10
Text_Y = 10

GameOver_Font = pygame.font.Font('freesansbold.ttf', 64)

def ShowScore(x, y):
    Score = Font.render('Score: ' + str(Score_Value), True, (255, 255, 255))
    Screen.blit(Score, (x, y))

def GameOverText():
    GameOvertext = GameOver_Font.render('Game Over', True, (255, 255, 255))
    Screen.blit(GameOvertext, (200, 250))

def Player(x, y):
    Screen.blit(Player_image, (x, y))

def Enemy(x, y, i):
    Screen.blit(Enemy_image[i], (x, y))

def FireBullet(x, y):
    global Bullet_State
    Bullet_State = 'fire'
    Screen.blit(Bullet_image, (x + 16, y + 10))

def Iscollision(Enemy_X, Enemy_Y, Bullet_X, Bullet_Y):
    distance = math.sqrt((Enemy_X - Bullet_X) ** 2 + (Enemy_Y - Bullet_Y) ** 2)
    return distance < Collision_Distance

running = True
while running:
    Screen.fill((0, 0, 0))
    Screen.blit(Background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Player_X_Change = -5
            if event.key == pygame.K_RIGHT:
                Player_X_Change = 5
            if event.key == pygame.K_SPACE and Bullet_State == "ready":
                Bullet_X = PlayerX
                Bullet_Y = PlayerY
                FireBullet(Bullet_X, Bullet_Y)
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                Player_X_Change = 0

    PlayerX += Player_X_Change
    PlayerX = max(0, min(PlayerX, Screen_Width - 64))

    for i in range(Number_of_Enemies):
        if Enemy_Y[i] > 340:
            for j in range(Number_of_Enemies):
                Enemy_Y[j] = 2000
            GameOverText()
            break

        Enemy_X[i] += Enemy_X_Change[i]
        if Enemy_X[i] <= 0 or Enemy_X[i] >= Screen_Width - 64:
            Enemy_X_Change[i] *= -1
            Enemy_Y[i] += Enemy_Y_Change[i]

        if Iscollision(Enemy_X[i], Enemy_Y[i], Bullet_X, Bullet_Y):
            global Score_Value
            Bullet_Y = Player_Start_Y
            Bullet_State = "ready"
            Score_Value += 1
            Enemy_X[i] = random.randint(0, Screen_Width - 64)
            Enemy_Y[i] = random.randint(Enemy_Start_Y_Min, Enemy_Start_Y_Max)

        Enemy(Enemy_X[i], Enemy_Y[i], i)

    if Bullet_Y <= 0:
        Bullet_Y = Player_Start_Y
        Bullet_State = "ready"
    if Bullet_State == "fire":
        FireBullet(Bullet_X, Bullet_Y)
        Bullet_Y -= Bullet_Y_Change

    Player(PlayerX, PlayerY)
    ShowScore(Text_X, Text_Y)
    pygame.display.update()
