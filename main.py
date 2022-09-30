import pygame
from pygame.locals import *
from circle import Circle
from knife import *


def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(
        surface, -angle, 1)  # Rotate the image.
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

    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    GREY = (100, 100, 100)

    global myScreen
    myScreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Example 1")

    kA = KnivesAirbourne(myScreen)
    knife_obj = Knife((0, 1), 10)
    kA.add(knife_obj)

    clock = pygame.time.Clock()

    move_left = False
    move_right = False
    move_up = False
    move_down = False
    # circle = pygame.image.load("circle.png").convert_alpha()
    # circle = pygame.transform.scale(circle, (200, 200) )

    circle = Circle((200, 200), [300, 300],  pygame.math.Vector2(0, 0))

    running = True

    while running:
        clock.tick(60)

        myScreen.fill(GREY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # if left click
                    kA.handle_click()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    circle.increase_speed()
                if event.key == pygame.K_DOWN:
                    circle.decrease_speed()

        kA.update()
        circle.show(myScreen)
        pygame.display.update()

     # pygame.display.flip()


if __name__ == '__main__':
    main()
