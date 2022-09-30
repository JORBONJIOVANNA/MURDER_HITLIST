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
    LIGHT_GREY = (60, 60, 60)
    DARK_RED = (107, 0, 0)
    BLACK = (0, 0, 0)

    global myScreen
    pygame.init()
    pygame.mixer.init()
    myScreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Example 1")

    clock = pygame.time.Clock()

    music = pygame.mixer.music.load(os.path.join(s, 'menu.mp3'))
    pygame.mixer.music.play(-1)
    change_music = False
    # circle = pygame.image.load("circle.png").convert_alpha()
    # circle = pygame.transform.scale(circle, (200, 200) )

    circle = Circle((200, 200), [300, 300],  pygame.math.Vector2(0, 0))

    kA = KnivesAirbourne(myScreen, circle)
    knife_obj = Knife((0, 1), 10)
    kA.add(knife_obj)
    running = True

    game_start = False

    small_font = pygame.font.SysFont('Verdana', 30)
    big_font = pygame.font.SysFont('Verdana', 45)
    game_name = big_font.render('KNIFE HIT', True, LIGHT_GREY)
    start_text = small_font.render('START', True, BLACK)

    while running:
        if change_music:
            pygame.mixer.music.play(-1)
            change_music = False

        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        myScreen.fill(GREY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_start:
                    if event.button == 1:  # if left click
                        kA.handle_click()
                elif SCREEN_WIDTH/3+30 <= mouse[0] <= SCREEN_WIDTH/3+170 and SCREEN_HEIGHT/2-100 <= mouse[1] <= SCREEN_HEIGHT/2-60:
                    game_start = True
                    change_music = True
                    music = pygame.mixer.music.load(
                        os.path.join(s, 'sound_1.mp3'))

            elif event.type == pygame.KEYDOWN and game_start:

                if event.key == pygame.K_UP:
                    circle.increase_speed()
                if event.key == pygame.K_DOWN:
                    circle.decrease_speed()

        if game_start:

            kA.update()
            circle.show(myScreen)
        else:
            pygame.draw.rect(myScreen, BLACK, [
                             SCREEN_WIDTH/4, SCREEN_HEIGHT/4-90, 300, 60])
            myScreen.blit(game_name, (SCREEN_WIDTH/4+30, SCREEN_HEIGHT/4-90))
            pygame.draw.rect(myScreen, DARK_RED, [
                             SCREEN_WIDTH/3+30, SCREEN_HEIGHT/2-100, 140, 40])
            myScreen.blit(start_text, (SCREEN_WIDTH/3+50, SCREEN_HEIGHT/2-100))

        pygame.display.update()

     # pygame.display.flip()


if __name__ == '__main__':
    main()
