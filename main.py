import pygame
from pygame.locals import *
import sys
from gameObjects import *
pygame

def main():
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

    FPS = 60

    pSizeX = 30
    pSizeY = 30

    BLUE = (0, 0, 255)

    global myScreen
    myScreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Example 1")

    # knife = pygame.image.load("./sword.png").convert_alpha()
    # dimensions = knife.get_size()
    # knife = pygame.transform.scale(knife, (dimensions[0]/8,dimensions[1]/8))
    # knife = pygame.transform.rotate(knife,180)
    # knife_obj = Knife((0,1),knife,10)
    kA = KnivesAirbourne(myScreen)
    knife_obj = Knife((0,1),10)

    clock = pygame.time.Clock()


    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False



    # (x, y) 


    running = True
    while running:
        
        clock.tick(60)
        myScreen.fill(BLUE)    
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #if left click 
                    kA.add(Knife((0,1),10))

        kA.update()
        pygame.display.update() 
    
    # pygame.display.flip()
    

if __name__ == '__main__': main()