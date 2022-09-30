import pygame
from pygame.locals import *
import sys
pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

FPS = 60

pSizeX = 30
pSizeY = 30

BLUE = (0, 0, 255)

myScreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Example 1")


clock = pygame.time.Clock()


moveLeft = False
moveRight = False
moveUp = False
moveDown = False



# (x, y) 


running = True
while running:
    
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        myScreen.fill(BLUE)    
        pygame.display.update() 
    
    # pygame.display.flip()
    
