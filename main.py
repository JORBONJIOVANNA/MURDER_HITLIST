import pygame
from pygame.locals import *
from circle import Circle
from knife import *
import os

def main():

    s = 'sound'
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600

    FPS = 60

    pSizeX = 30
    pSizeY = 30

    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    GREY = (100, 100, 100)

    global myScreen
    pygame.mixer.init()
    myScreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Example 1")

    clock = pygame.time.Clock()

    music = pygame.mixer.music.load(os.path.join(s, 'sound_1.mp3'))
    pygame.mixer.music.play(-1)
    # circle = pygame.image.load("circle.png").convert_alpha()
    # circle = pygame.transform.scale(circle, (200, 200) )

    circle = Circle((200, 200), [300, 300],  pygame.math.Vector2(0, 0))

    kA = KnivesAirbourne(myScreen, circle)
    knife_obj = Knife((0, 1), 10)
    kA.add(knife_obj)

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
