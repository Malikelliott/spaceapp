import random
from turtledemo.nim import SCREENWIDTH, SCREENHEIGHT

import pygame
import math
import self
from pygame import mixer

#INITIALIZATION
pygame.init()

#SCREEN
SCREENWIDTH = 800
SCREENHEIGHT = int(SCREENWIDTH * 0.8)
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))


#TITLE (displays the title when you open this)
pygame.display.set_caption("Asteroid Dodge")

#buttons
pauseButton = pygame.Rect((625, 10, 150, 50))

#MUSIC (plays during the minigame and -1 means it loops indefinitely)
#mixer.music.load('')
#mixer.music.play(-1)


#PLAYER
ufoImg = pygame.image.load('ufo.png')
player1 = pygame.image.load('Player1.png')
player1X = 75
player1Y = 600
move_speed = 0.75
def player(x,y):
    screen.blit(player1, (player1X, player1Y))

#ASTEROID
asteroidImg1 = pygame.image.load('asteroid-shape.png')
AsteroidX = random.randint(10,790)
AsteroidY = random.randint(10,20)
xAsteroidChange = 0.5
yAsteroidChange = 0.3



def asteroid(x,y):
    screen.blit(asteroidImg1, (AsteroidX, AsteroidY))

def ufo():
    screen.blit(ufoImg,(400,400))

#SCORE
score = 0 #set variable for score
font = pygame.font.Font('freesansbold.ttf', 32) #text font and font size
textX = 10 #X position of the text
textY = 10 #Y position of the text

def show_score(x,y):
    scoretxt = font.render("Score: " + str(score),True,(0,255,255)) # rendering the text (what it says and the colour
    screen.blit(scoretxt, (x,y))#puts the text on the screen

#GameLoop
run = True
while run:

    screen.fill((0,0,64)) #screen resets each time
    #pygame.draw.rect(screen, (255,0,0), player1)
    player(player1X,player1Y)
    asteroid(AsteroidX,AsteroidY)

    AsteroidY += yAsteroidChange
    AsteroidX += xAsteroidChange
    player1Y -= 0.25

    key = pygame.key.get_pressed()

    #Player Movement
    if key[pygame.K_a] | key[pygame.K_LEFT] == True:
        player1X -= move_speed
    elif key[pygame.K_d] | key[pygame.K_RIGHT] == True:
        player1X += move_speed
    elif key[pygame.K_w] | key[pygame.K_UP]== True:
        player1Y -= move_speed
    elif key[pygame.K_s] | key[pygame.K_DOWN] == True:
        player1Y += move_speed

    if player1X <= 25:
        player1X = 25
    elif player1X >= (SCREENWIDTH) - 75 :
        player1X = (SCREENWIDTH) - 75

    if player1Y <= 25:
        player1Y = 25
    elif player1Y >= SCREENHEIGHT - 75:
        player1Y = SCREENHEIGHT - 75

    if AsteroidY >SCREENHEIGHT:
        AsteroidY = 0
        score += 1
        yAsteroidChange += 0.1
        #screen.blit(asteroidImg1.copy(),(AsteroidX + 50,AsteroidY))


    if AsteroidX > SCREENWIDTH:
        xAsteroidChange = -0.5
    elif AsteroidX < 0:
        xAsteroidChange = 0.5

    if (((player1X - AsteroidX < 25) & (player1X - AsteroidX > -25)) &
            ((player1Y - AsteroidY < 25) & (player1Y - AsteroidY > -25))): #if hit
        pygame.quit()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    show_score(textX,textY)

    pygame.display.update()

pygame.quit()