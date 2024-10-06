import random
from turtledemo.nim import SCREENWIDTH, SCREENHEIGHT

import pygame
import math
from pygame import mixer

#Initialize the game
pygame.init()

#create screen
SCREENWIDTH = 800
SCREENHEIGHT = int(SCREENWIDTH * 0.8)
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))


#Title
pygame.display.set_caption("ZeroG Capture the Flag")


#MUSIC (plays during the minigame and -1 means it loops indefinitely)
#mixer.music.load('')
#mixer.music.play(-1)

#flags
team1flag = pygame.image.load('red-flag.png')
team2flag = pygame.image.load('blueflag.png')
team1flagX = 700.0
team1flagY = 25.0
team2flagX = 100.0
team2flagY = 25.0
redCaught = False
blueCaught = False


#The player
ufoImg = pygame.image.load('ufo.png')
player1 = pygame.image.load('Player1.png')
player1X = 75.0
player1Y = 600.0

player2 = pygame.image.load('Player2.png')
player2X = 725.0
player2Y = 600.0


move_speed = 0.3 #how fast the player can move left and right
#this must be higher than the no gravity force applied to the character so that they can move down

def player(x,y):
    screen.blit(player1, (player1X, player1Y))
    screen.blit(player2, (player2X, player2Y))

team1zone = pygame.Rect((75, 600, 100, 100))
team2zone = pygame.Rect((625, 600, 100, 100))

#Asteroid
asteroidImg1 = pygame.image.load('asteroid-shape.png')
AsteroidX = random.randint(10,790)
AsteroidY = 400
xAsteroidChange = 0.5
yAsteroidChange = 0.3

def asteroid(x, y):
    screen.blit(asteroidImg1, (x, y))

def ufo():
    screen.blit(ufoImg,(400,400))

def flags():
    screen.blit(team1flag,(team1flagX,team1flagY))
    screen.blit(team2flag, (team2flagX, team2flagY))


font = pygame.font.Font('freesansbold.ttf', 32)

def show_win(x,y):
    winTxt = font.render("You win! Congratulations!" ,True,(0,255,0))
    screen.blit(winTxt, (x,y))

def show_lose(x,y):
    loseTxt = font.render("You lost! Sorry!" ,True,(255,0,255))
    screen.blit(loseTxt, (x,y))

#GameLoop
run = True
while run:

    screen.fill((0,0,64)) #screen resets each time
    mouse_pos = pygame.mouse.get_pos()
    flags() #draw both flags
    player(player1X, player1Y) #draw player 1 at their starting point
    player(player2X, player2Y) #draw player 2 at their starting point
    pygame.draw.rect(screen, (255,0,0), team1zone)
    pygame.draw.rect(screen, (0, 0, 255), team2zone)


    #####################OBSTACLE MOVEMENT#####################
    asteroid(AsteroidX,AsteroidY) #draw asteroid

    #Have the asteroid bounce around the screen
    AsteroidY += yAsteroidChange
    AsteroidX += xAsteroidChange

    if AsteroidY >SCREENHEIGHT:
        AsteroidY = 0
        #score += 1
        #xAsteroidChange += 0.1
        #screen.blit(asteroidImg1.copy(),(AsteroidX + 50,AsteroidY))

    if AsteroidX > SCREENWIDTH:
        xAsteroidChange = -0.5
    elif AsteroidX < 0:
        xAsteroidChange = 0.5


    ######################## Player 1 Movement  ########
    player1Y -= 0.25 # have the player constantly float upward slowly to emulate no gravity

    key = pygame.key.get_pressed()
    if key[pygame.K_a] | key[pygame.K_LEFT] == True:
        player1X -= move_speed
    elif key[pygame.K_d] | key[pygame.K_RIGHT] == True:
        player1X += move_speed
    #elif key[pygame.K_w] | key[pygame.K_UP] == True:
        #player1Y -= move_speed
    elif key[pygame.K_s] | key[pygame.K_DOWN] == True:
        player1Y += move_speed

    # Keep Player 1 from flying of the screen
    if player1X <= 25:
        player1X = 25
    elif player1X >= (SCREENWIDTH) - 75:
        player1X = (SCREENWIDTH) - 75

    if player1Y <= 25:
        player1Y = 25
    elif player1Y >= SCREENHEIGHT - 75:
        player1Y = SCREENHEIGHT - 75

    #player 1 can capture their flag with the space key when they are touching the flag
    if (((player1X - team1flagX < 5) & (player1X - team1flagX > -5)) &
        ((player1Y - team1flagY < 5) & (player1Y - team1flagY > -5))):
        if key[pygame.K_SPACE]:
            redCaught = True


    #Player 1 Drops their flag when hit by an asteroid
    if (((player1X - AsteroidX < 25) & (player1X - AsteroidX > -25)) &
        ((player1Y - AsteroidY < 25) & (player1Y - AsteroidY > -25))):
        redCaught = False

    # When the player catches the flag
    if redCaught:
        team1flagX = player1X #link the red flag to player 1
        team1flagY = player1Y
        if team1flagY > SCREENHEIGHT - 76:
                show_win(200,300) #show winning text
                team1flagX = 125 #plant the flag on the base
                team1flagY = 725
                player1Y += 1 #stop player 1 from floating
                AsteroidX = 400 #freeze the asteroid
                AsteroidY = 400
                player2X = 0 #freeze player 2
                player2Y = 0
    else:
        team1flagY -= 1

    if team1flagY <= 25:
        team1flagY = 25
    elif team1flagY >= SCREENHEIGHT - 75:
        team1flagY = SCREENHEIGHT - 75

    ########################## AI Movement ##################

    #keep player 2 from falling off the screen
    if player2Y >= SCREENHEIGHT - 75:
        player2Y = SCREENHEIGHT - 75

    #player 2 is hit by asteroid and drops their flag
    if (((player2X - AsteroidX < 25) & (player2X - AsteroidX > -25)) &
        ((player2Y - AsteroidY < 25) & (player2Y - AsteroidY > -25))):
        blueCaught = False

    #When player 2 captures their flag
    if blueCaught:
        team2flagX = player2X #link the blue flag to player 2
        team2flagY = player2Y
        newDirection_x = 725 - player2X #set player 2's destination to their base
        newDirection_y = 600 - player2Y
        newDistance = math.hypot(newDirection_x, newDirection_y)  # Get distance to target
        if newDistance > 0: #while player 2 is moving to their base
            newDirection_x /= newDistance
            newDirection_y /= newDistance
            player2X += newDirection_x * 0.07
            player2Y += newDirection_y * 0.07
            if team2flagY > SCREENHEIGHT - 76: #when player 2 reaches their base first
                show_lose(250,300) #show losing text
                team2flagX = 675 #plant the flag on the base
                team2flagY = 725
                player2Y += 1 #stop player 2 from floating
                AsteroidX = 400 #freeze the asteroid
                AsteroidY = 400
                player1X = 0 #freeze player 1
                player1Y = 0
    else: #when player 2 doesn't have their flag captured
        team2flagY -= 1 #player 2's flag floats upward
        direction_x = team2flagX - player2X #set player 2's destination to the flag
        direction_y = team2flagY - player2Y
        distance = math.hypot(direction_x, direction_y)

        if distance > 0: #while heading to the flag
            direction_x /= distance
            direction_y /= distance
            player2X += direction_x * 0.1
            player2Y += direction_y * 0.1
            if distance < 0.1:
                blueCaught = True # set captured to true when player 2 reaches their flag

    #Keeps player 2's flag from going out of bounds
    if team2flagY <= 25:
        team2flagY = 25
    elif team2flagY >= SCREENHEIGHT - 75:
        team2flagY = SCREENHEIGHT - 75

    # keeps the window open
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()