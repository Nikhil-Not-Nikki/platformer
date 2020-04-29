import pygame
import numpy


x = 0
size = 62
rightPressed = False
leftPressed = False
delay = 1
screenX = 960
screenY = 520
y = screenY - size
acceleration = 5
jumpVelocity = 0
xVelocity = 5
hasJumped = 0
upLeft = (-1,1)
up = (0,1)
upRight = (1,1)
right = (1,0)
downRight = (-1,1)
down = (0,-1)
downLeft = (-1,-1)
left = (-1,0)
neutral = (0,0)
direction = [0,0]
dashLength = 0
dashSpeed = 5
charRect = pygame.Rect(x, y, size, size)
platforms = (pygame.Rect(50, screenY-84, 100, 20), pygame.Rect(50, screenY-200, 100, 20))
black = (0,0,0)
white = (255,255,255)


def main():

    pygame.init()

    pygame.display.set_caption("Platformer")
    screen = pygame.display.set_mode((screenX,screenY))

    running = True
    MOVEEVENT = pygame.USEREVENT+1
    GRAVEVENT = pygame.USEREVENT+2
    global rightPressed
    global leftPressed
    global x
    global y
    global jumpVelocity
    global hasJumped
    global dashLength
    global direction
    global charRect

    pygame.time.set_timer(MOVEEVENT, delay)
    pygame.time.set_timer(GRAVEVENT, 1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    rightPressed = True
                    direction[0] = 1
                if event.key == pygame.K_LEFT:
                    leftPressed = True
                    direction[0] = -1
                if event.key == pygame.K_SPACE:
                    if hasJumped < 2:
                        jumpVelocity = 200
                        hasJumped += 1
                if event.key == pygame.K_f:
                    dashLength += 50
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    rightPressed = False
                    direction[0] = 0
                if event.key == pygame.K_LEFT:
                    leftPressed = False
                    direction[0] = 0
            if event.type == MOVEEVENT:
                x = moveX(x)
                x = dashX(x)
                #y = dashY(y)
            if event.type == GRAVEVENT:
                y = moveY(y)
            if event.type == pygame.QUIT:
                running = False
        #get direction
        keys = pygame.key.get_pressed()
        #if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            #direction = upRight
        #if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            #direction = upLeft
        screen.fill(white)
        charRect = pygame.Rect(x, y, size, size)
        for plat in platforms:
            pygame.draw.rect(screen, black, plat)
        pygame.draw.rect(screen, black, charRect)
        pygame.display.flip()

def checkSign(num):
    if num > 0:
        return 1
    if num < 0:
        return -1
    if num == 0:
        return 0

def moveX(x):
    global y
    if rightPressed:
        x += xVelocity
    if leftPressed:
        x -= xVelocity
    currentBound = bounds(x, y)
    x = currentBound[0]
    y = currentBound[1]
    return x

def bounds(x,y):
    global charRect
    global jumpVelocity
    global hasJumped
    global charRect
    if y >= (screenY - size):
        y = (screenY - size)
        jumpVelocity = 0
        hasJumped = 0
    if y < 0:
        y = 0
    for plat in platforms:
        if charRect.colliderect(plat):
            if plat.y < y:
                while charRect.colliderect(plat):
                    x += direction[0]
                    y += direction[1]
                    charRect = pygame.Rect(x, y, size, size)
                jumpVelocity = 0
            if plat.y > y:
                while charRect.colliderect(plat):
                    x += direction[0]
                    y += direction[1]
                    charRect = pygame.Rect(x, y, size, size)
                jumpVelocity = 0
                hasJumped = 0
    while x > (screenX - size):
        x -= 1
    while x < 0:
        x += 1
    for plat in platforms:
        if charRect.colliderect(plat):
            if plat.x < x:
                while charRect.colliderect(plat):
                    x += direction[0]
                    y += direction[1]
                    charRect = pygame.Rect(x, y, size, size)
            if plat.x > x:
                while charRect.colliderect(plat):
                    x += direction[0]
                    y += direction[1]
                    charRect = pygame.Rect(x, y, size, size)
    return (x,y)

def moveY(y):
    global jumpVelocity
    global hasJumped
    global x
    decY = float(y)
    decY -= (float(jumpVelocity) / 50.000)
    jumpVelocity -= acceleration
    direction[1] = checkSign(jumpVelocity)
    y = int(decY)
    currentBound = bounds(x,y)
    x = currentBound[0]
    y = currentBound[1]
    return y


def dashX(x):
    global dashLength
    global y
    if dashLength > 0:
        for k in range (0, dashSpeed * abs(direction[0])):
            x = moveX(x)
            currentBound = bounds(x, y)
            x = currentBound[0]
            y = currentBound[1]
        dashLength -= dashSpeed
    return x

def dashY(y):
    global dashLength
    if dashLength > 0:
        for k in range(0, dashSpeed * abs(direction[1])):
            y += -3 * direction[1]
        dashLength -= dashSpeed
    return y


if __name__=="__main__":
    main()