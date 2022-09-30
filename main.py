import pygame
from pygame.locals import *
import sys
from gameObjects import *
pygame

def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

def main():
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

    FPS = 60

    pSizeX = 30
    pSizeY = 30

    GREY = (100, 100, 100)

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
    # circle = pygame.image.load("circle.png").convert_alpha()
    # circle = pygame.transform.scale(circle, (200,200))
    circle = Circle(myScreen)
    # pygame.draw.polygon(circle, pygame.Color('dodgerblue3'), ((0, 0), (140, 30), (0, 60)))
    # pivot = [300, 300]
    # offset = pygame.math.Vector2(0, 0)
    # angle = 0
    # speed = 2

    running = True
    while running:
        
        clock.tick(60)
        myScreen.fill(GREY)    
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #if left click 
                    kA.add(Knife((0,1),10))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if speed > 16:
                        speed = 12
                    else:
                        speed += 2
                if event.key == pygame.K_DOWN:
                    if speed < 4:
                        speed = 2
                    else:
                        speed -= 2
            
        # angle += speed
        # rotated_image, rect = rotate(circle, angle, pivot, offset)
        # myScreen.blit(rotated_image, rect)
        circle.rotate_circle()
        kA.update()
        pygame.display.update() 
    
    # pygame.display.flip()
    

if __name__ == '__main__': main()