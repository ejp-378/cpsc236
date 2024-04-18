#DODGER GAME VARIANT
#CHANGES MADE BY ELI PODGORSKI

import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600   #width of game window
WINDOWHEIGHT = 600  #height of game window
TEXTCOLOR = (255, 255, 255) #RGB tuple
BACKGROUNDCOLOR = (0, 0, 0) #RGB tuple
FPS = 40    #Frames per second, controls games refresh rate
BADDIEMINSIZE = 10  
BADDIEMAXSIZE = 40  
BADDIEMINSPEED = 1  
BADDIEMAXSPEED = 8

# New Constants
ADDNEWBADDIERATE = 6    #Frequency at which baddies are added
PLAYERMOVERATE = 5      #how fast player can move
ADDNEWPOWERUPRATE = 500 #Controls how often power ups spawn
POWERUPSPEED = 5        #Speed of powerups
ADDNEWDOUBLEPOWERRATE = 600    #Rate of 2x points powerup spawning
DOUBLEPOWERDURATION = 500      #Duration of 2x points power up


#exits game
def terminate():
    pygame.quit()
    sys.exit()

#Holds game until a key is pressed
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

#Checks for collisons between baddie and player
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

#Renders text on surface
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# set up images
playerImage = pygame.image.load('player.png')
playerImage = pygame.transform.scale(playerImage, (30,30))
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')


#try - except statements for the power up images
try:
    powerUpImage = pygame.image.load('clearscreen1.jpg')
    powerUpImage = pygame.transform.scale(powerUpImage, (50,50))
    
except pygame.error as e:
    print(f"Cannot load image: {e}")
    terminate()   
powerUpRect = powerUpImage.get_rect()

try:
    doublePowerUpImage = pygame.image.load('2xpoints.png')
    doublePowerUpImage = pygame.transform.scale(doublePowerUpImage, (50, 50))
except pygame.error as e:
    print(f"Cannot load image: {e}")
    terminate
doublePowerUpRect = doublePowerUpImage.get_rect()


# show the "Start" screen
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
    # set up the start of the game
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    
    powerUpAddCounter = 0
    powerUpActive = False
    
    doublePowerUpAddCounter = 0
    doublePowerUpActive = False
    doublePowerUpCounter = 0
    doubleScoreActive = False
    
    pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop runs while the game part is playing
        
        #score += 1 # increase score, original score line
        
        if doubleScoreActive:
            score += 2
        else:
            score += 1
        
        windowSurface.fill(BACKGROUNDCOLOR)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):   #makes baddies go up the screen if z is pressed
                    reverseCheat = True
                if event.key == ord('x'):   #makes baddies go slow if x is pressed
                    slowCheat = True
                
                #Controls player movement using WASD
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            #reverts game to normal if z or x is let go, if escape is hit, game is terminated
            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)

        #adds clearscreen power up to the screen at a random position
        powerUpAddCounter += 1
        if powerUpAddCounter >= ADDNEWPOWERUPRATE:
            #print("Adding power up")
            powerUpAddCounter = 0
            max_x_position = max(0, WINDOWWIDTH - powerUpRect.width)
            powerUpRect.topleft = (random.randint(0, max_x_position), 0 - powerUpRect.height)
            powerUpActive = True
            
        #adds 2x points power up to screen at a random position
        doublePowerUpAddCounter += 1
        if doublePowerUpAddCounter >= ADDNEWDOUBLEPOWERRATE:
            #print("Adding power up")
            doublePowerUpAddCounter = 0
            doublePowerUpRect.topleft = (random.randint(0, max_x_position), 0 - doublePowerUpRect.height)
            doublePowerUpActive = True
        
        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        #moves clearscreen power up down the screen at POWERUPSPEED
        if powerUpActive:
            #print("moving power up")
            powerUpRect.move_ip(0, POWERUPSPEED)
            if powerUpRect.top > WINDOWHEIGHT:
                powerUpActive = False
                
        #checks if player and power up collide, if they do the baddies are cleared from the scren
        if powerUpActive and playerRect.colliderect(powerUpRect):
            powerUpActive = False
            baddies.clear()
            
        #draws clearscreen powerup
        if powerUpActive:
            #print("drawing power up")
            windowSurface.blit(powerUpImage, powerUpRect)
        
        #moves 2x points powerup down the screen at POWERUPSPEED
        if doublePowerUpActive:
            #print("moving power up")
            doublePowerUpRect.move_ip(0, POWERUPSPEED)
            if doublePowerUpRect.bottom > WINDOWHEIGHT:
                doublePowerUpActive = False
        
        #checks if player and 2x point powerup collide, if they do the double score is activated for the DOUBLEPOWERDURATION
        if doublePowerUpActive and playerRect.colliderect(doublePowerUpRect):
            doublePowerUpActive = False
            doubleScoreActive = True
            doublePowerUpCounter = DOUBLEPOWERDURATION
            
        if doubleScoreActive:
            doublePowerUpCounter -= 1
            if doublePowerUpCounter <= 0:
                doubleScoreActive = False
        
        #draws 2x point powerup
        if doublePowerUpActive:
            #print("drawing power up")
            windowSurface.blit(doublePowerUpImage, doublePowerUpRect)
            
            
        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        


        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
