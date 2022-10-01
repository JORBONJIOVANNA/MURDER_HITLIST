import pygame
from pygame.locals import *
from circle import Circle
from knife import *
import os


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

pygame.init()
pygame.mixer.init()
myScreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("KNIFE HIT")


BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
LIGHT_GREY = (60, 60, 60)
DARK_RED = (107, 0, 0)
BLACK = (0, 0, 0)

high_score = 0
user_score = 0
game_over = False

level_goal = 2
knife_added = 0

circle_1_path = "circle.png"
circle_2_path = "circle_2.png"

circle_1 = pygame.image.load(
    "resources/{}".format(circle_1_path)).convert_alpha()
circle_1 = pygame.transform.scale(circle_1, (100, 100))

circle_2 = pygame.image.load(
    "resources/{}".format(circle_2_path)).convert_alpha()
circle_2 = pygame.transform.scale(circle_2, (100, 100))

small_font = pygame.font.SysFont('Helvetica', 30)
big_font = pygame.font.Font('fonts/PPEditorialNew-Ultralight.otf', 45)
game_name = big_font.render('KNIFE HIT', True, WHITE)
start_text = small_font.render('START', True, BLACK)
customize_text = small_font.render('CUSTOMIZE', True, BLACK)
choose_text = small_font.render('CHOOSE', True, BLACK)


def menu_screen(tick, image_index, myScreen, customization_screen, last_score=-1):
    mouse_pos = pygame.mouse.get_pos()

    if tick == 5:
        tick = 0
        image_index += 1
        if image_index > 11:
            image_index = 1
        menu_img = pygame.image.load(
            "resources/menu_images/frame_{}.gif".format(image_index)).convert_alpha()
        menu_img = pygame.transform.scale(menu_img, (600, 600))
        myScreen.blit(menu_img, (0, 0))

    pygame.draw.rect(myScreen, BLACK, [
        SCREEN_WIDTH/4, SCREEN_HEIGHT/4-90, 300, 60])

    if last_score == -1:
        game_name_rect = game_name.get_rect(center=(SCREEN_WIDTH/2, 80))
        myScreen.blit(game_name, game_name_rect)
    else:
        last_score_text = big_font.render(
            "SCORE: {}".format(last_score), True, WHITE)
        last_score_rect = last_score_text.get_rect(
            center=(SCREEN_WIDTH/2, 80))
        myScreen.blit(last_score_text, last_score_rect)

    if customization_screen:

        start_rect = pygame.draw.rect(myScreen, DARK_RED, [
            SCREEN_WIDTH/3+30, SCREEN_HEIGHT/2-100, 140, 40])

        start_text = small_font.render('START', True, BLACK)

        if start_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            start_text = small_font.render('START', True, WHITE)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        myScreen.blit(start_text, (SCREEN_WIDTH/3+50, SCREEN_HEIGHT/2-90))

        myScreen.blit(circle_1, (SCREEN_WIDTH/6, SCREEN_HEIGHT/2))
        myScreen.blit(circle_2, (SCREEN_WIDTH/2+100, SCREEN_HEIGHT/2))
        pygame.draw.rect(myScreen, DARK_RED, [
            SCREEN_WIDTH/2+100, SCREEN_HEIGHT-150, 140, 40])
        myScreen.blit(choose_text, (SCREEN_WIDTH/2+100, SCREEN_HEIGHT-140))

        # pygame.draw.rect(myScreen, DARK_RED, [
        #                 SCREEN_WIDTH/3, SCREEN_HEIGHT/2, 200, 40])
        # myScreen.blit(choose_text, (SCREEN_WIDTH/3+10, SCREEN_HEIGHT/2))

    else:
        start_rect = pygame.draw.rect(myScreen, DARK_RED, [
            SCREEN_WIDTH/3+30, SCREEN_HEIGHT/2-100, 140, 40])

        start_text = small_font.render('START', True, BLACK)

        if start_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            start_text = small_font.render('START', True, WHITE)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        myScreen.blit(start_text, (SCREEN_WIDTH/3+50, SCREEN_HEIGHT/2-90))

        customize_rect = pygame.draw.rect(myScreen, DARK_RED, [
            SCREEN_WIDTH/3, SCREEN_HEIGHT/2, 200, 40])
        customize_text = small_font.render('CUSTOMIZE', True, BLACK)

        if customize_rect.collidepoint(mouse_pos):
            customize_text = small_font.render('CUSTOMIZE', True, WHITE)

        myScreen.blit(customize_text, (SCREEN_WIDTH /
                      3+10, SCREEN_HEIGHT/2 + 10))

        high_score_text = small_font.render(
            'HIGH SCORE: {}'.format(high_score), True, BLACK)
        pygame.draw.rect(myScreen, DARK_RED, [
            SCREEN_WIDTH/3-30, SCREEN_HEIGHT-100, 300, 40])
        myScreen.blit(high_score_text, (SCREEN_WIDTH/3-10, SCREEN_HEIGHT-90))

        if customize_rect.collidepoint(mouse_pos) or start_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    return tick, image_index


def load_level(level, circle):

    global user_score
    global game_over
    global knife_added

    # if num == 1:

    myScreen.fill(DARK_RED)

    game_over, user_score, knife_added = kA.update(user_score, knife_added)

    # temporary, so after level 1 we add randomness to the circle movement
    # implemented in circle.update()
    if level > 3:
        circle.show(myScreen, 1)
    else:
        circle.show(myScreen, 0)

    score_text = big_font.render(
        '{}'.format(user_score), True, WHITE)

    level_text = small_font.render(
        'LEVEL {}'.format(level), True, WHITE)

    pass_info_text = small_font.render(
        "{}/{}".format(knife_added, level_goal), True, WHITE)

    score_rect = score_text.get_rect(
        center=(SCREEN_WIDTH / 2, 80))
    myScreen.blit(score_text, score_rect)
    myScreen.blit(level_text, (30, SCREEN_HEIGHT-60))

    pass_info_rect = pass_info_text.get_rect(
        right=SCREEN_WIDTH - 30, y=SCREEN_HEIGHT - 60)
    myScreen.blit(pass_info_text, pass_info_rect)


def main():

    s = 'sound'
    # SCREEN_WIDTH = 600
    # SCREEN_HEIGHT = 600

    FPS = 60

    pSizeX = 30
    pSizeY = 30

    global myScreen
    global high_score
    global kA
    global game_over
    global user_score
    global knife_added
    global level_goal

    circle_path = circle_1_path
    clock = pygame.time.Clock()

    music = pygame.mixer.music.load(os.path.join(s, 'menu.mp3'))
    knife_effect = pygame.mixer.Sound(os.path.join(s, 'knife_effect.flac'))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    knife_effect.set_volume(0.2)
    change_music = False

    running = True

    game_start = False

    tick = 0
    image_index = 1
    start_image_index = 0
    start_animation = False
    level = 1
    last_score = -1
    next_level = True
    next_goal = 2

    circle = Circle((200, 200), [300, 300],
                    pygame.math.Vector2(0, 0), 2, circle_path)

    kA = KnivesAirbourne(myScreen, circle, level)
    knife_obj = Knife((0, 1), 10)
    kA.add(knife_obj)
    customization_screen = False

    while running:
        pygame.display.update()
        # get high score
        with open("high_scores.txt", 'r+') as w:
            lines = w.readlines()
            high_score = int(lines[-1])

        if change_music:
            pygame.mixer.music.play(-1)
            change_music = False

        clock.tick(60)
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_start:
                    if event.button == 1:  # if left click
                        pygame.mixer.Sound.play(knife_effect)
                        kA.handle_click()

                elif SCREEN_WIDTH/3+30 <= mouse[0] <= SCREEN_WIDTH/3+170 and SCREEN_HEIGHT/2-100 <= mouse[1] <= SCREEN_HEIGHT/2-60:
                    start_animation = True

                elif SCREEN_WIDTH/3 <= mouse[0] <= SCREEN_WIDTH/3+200 and SCREEN_HEIGHT/2 <= mouse[1] <= SCREEN_HEIGHT/2+40:
                    customization_screen = True

                # if user chooses bowling ball
                elif SCREEN_WIDTH/2+100 <= mouse[0] <= SCREEN_WIDTH/2+240 and SCREEN_HEIGHT-150 <= mouse[1] <= SCREEN_HEIGHT-110 and customization_screen:
                    circle_path = circle_2_path
                    circle = Circle((200, 200), [300, 300],  pygame.math.Vector2(
                        0, 0), level+3, circle_path)

            # elif event.type == pygame.KEYDOWN and game_start:

            #     if event.key == pygame.K_UP:
            #         circle.increase_speed()
            #     if event.key == pygame.K_DOWN:
            #         circle.decrease_speed()

        if game_start and not(start_animation):

            if knife_added >= level_goal and next_level:
                level += 1

                # level 2 music
                pygame.mixer.music.load(os.path.join(s, 'sound_2.mp3'))
                change_music = True

                # this is to reset everything and add new knives and circle
                circle = Circle((200, 200), [300, 300],  pygame.math.Vector2(
                    0, 0), level+3, circle_path)
                kA = KnivesAirbourne(myScreen, circle, level)
                knife_obj = Knife((0, 1), 10)
                kA.add(knife_obj)
                next_level = True
                level_goal = min(level + 1, 50)
                next_goal += level_goal
                knife_added = 0
                # continue coz we need to get rid of the old stuff by sending it to the pygame.update line
                # with this continue keyword
                continue
            load_level(level, circle)

            # resets game
            if game_over:
                if user_score > high_score:
                    high_score = user_score
                    with open("high_scores.txt", 'w') as w:
                        w.write(str(high_score))

                last_score = user_score
                user_score = 0
                game_start = False
                tick = 0
                level = 1
                level_goal = 2
                next_goal = 2
                knife_added = 0
                start_image_index = 0
                myScreen.fill((0, 0, 0))
                kA = KnivesAirbourne(myScreen, circle, level)
                knife_obj = Knife((0, 1), 10)
                kA.add(knife_obj)

                change_music = True
                music = pygame.mixer.music.load(os.path.join(s, 'menu.mp3'))
        else:
            tick, image_index = menu_screen(
                tick, image_index, myScreen, customization_screen, last_score)

            if start_animation:

                start_image_index += 1

                # coz there are 150 pictures for that animation, we wanna stop once we are done with them
                if start_image_index > 150:
                    start_animation = False
                    game_start = True
                    change_music = True
                    music = pygame.mixer.music.load(
                        os.path.join(s, 'sound_1.mp3'))
                transition = pygame.image.load(
                    "resources/start_animation/frame_{:03d}_delay-0.03s.gif".format(start_image_index)).convert_alpha()
                transition = pygame.transform.scale(transition, (600, 600))
                myScreen.blit(transition, (0, 0))

        tick += 1
     # pygame.display.flip()


if __name__ == '__main__':
    main()
