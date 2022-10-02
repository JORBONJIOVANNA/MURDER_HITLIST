import pygame
from pygame.locals import *
from circle import Circle
from knife import *
import os
from inventory import *
import random

# Leaderboard variables
leaderboard = False
GREEN = (0, 255, 0)
# Leaderboard variables

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

pygame.init()
pygame.mixer.init()
myScreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MURDERER HITLIST")

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
LIGHT_GREY = (60, 60, 60)
DARK_RED = (107, 0, 0)
BLACK = (0, 0, 0)
NEW_BLACK = (58, 58, 58)

high_score = 0
user_score = 0
game_over = False
level_color = DARK_RED

level_goal = 2
knife_added = 0
score_list = []
rank = 11
name_input = ''
write_name = False
option_1 = False
option_2 = False
last_level = 1

circle_1_path = "circle.png"
circle_2_path = "circle_2.png"

circle_1 = pygame.image.load(
    "resources/{}".format(circle_1_path)).convert_alpha()
circle_1 = pygame.transform.scale(circle_1, (100, 100))

circle_2 = pygame.image.load(
    "resources/{}".format(circle_2_path)).convert_alpha()
circle_2 = pygame.transform.scale(circle_2, (100, 100))

powerup_1 = pygame.image.load(
    "resources/game_icons/slow_menu.png").convert_alpha()
powerup_1 = pygame.transform.scale(powerup_1, (75, 75))

powerup_2 = pygame.image.load(
    "resources/game_icons/shrink_menu.png").convert_alpha()
powerup_2 = pygame.transform.scale(powerup_2, (75, 75))

powerup_3 = pygame.image.load(
    "resources/game_icons/extra_active.png").convert_alpha()
powerup_3 = pygame.transform.scale(powerup_3, (75, 75))

knife = pygame.image.load("resources/sword.png").convert_alpha()
knife = pygame.transform.scale(knife, (50, 75))

smallest_font = pygame.font.SysFont('Helvetica', 27)
small_font = pygame.font.SysFont('Helvetica', 30)
big_font = pygame.font.Font('fonts/PPEditorialNew-Ultralight.otf', 45)
game_name = big_font.render('MURDERER HITLIST', True, WHITE)

start_text = small_font.render('START', True, BLACK)
customize_text = small_font.render('CUSTOMIZE', True, BLACK)
choose_text = small_font.render('CHOOSE', True, BLACK)

# When game asks for user input, this is purely rendering the screen


def insert_name(tick, image_index, myScreen, level):
    global name_input
    global rank
    global smallest_font
    global SCREEN_HEIGHT
    global SCREEN_WIDTH

    # Rendering
    if tick % 6 == 5:
        tick = 0
        image_index += 1
        if image_index > 11:
            image_index = 1
        menu_img = pygame.image.load(
            "resources/menu_images/frame_{}.gif".format(image_index)).convert_alpha()
        menu_img = pygame.transform.scale(menu_img, (600, 600))
        myScreen.blit(menu_img, (0, 0))

    success_message_1 = smallest_font.render(
        'Well done Murderer!', True, WHITE)
    success_message_2 = smallest_font.render(
        'You reached level {} which is rank {}!'.format(level, rank+1), True, WHITE)
    success_message_3 = smallest_font.render(
        'Please enter your name to go on Serial Killer List:', True, WHITE)
    myScreen.blit(success_message_1,
                  (SCREEN_WIDTH/3 - 20, SCREEN_HEIGHT/3-100))
    myScreen.blit(success_message_2,
                  (SCREEN_HEIGHT/4 - 30, SCREEN_HEIGHT/3-70))
    myScreen.blit(success_message_3, (50, SCREEN_HEIGHT/3-40))

    pygame.draw.rect(myScreen, DARK_RED, [
                     SCREEN_WIDTH/4, SCREEN_HEIGHT/2-100, SCREEN_WIDTH/2, 40])

    if(pygame.time.get_ticks() % 1000 < 500):
        name_output = smallest_font.render(name_input, True, WHITE)
    else:
        name_output = smallest_font.render(name_input + "|", True, WHITE)

    myScreen.blit(name_output, (SCREEN_WIDTH/4+5, SCREEN_HEIGHT/3+5))

    return tick, image_index


def menu_screen(tick, image_index, myScreen, customization_screen, leaderboard, last_level):

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

    if not(leaderboard) and not(customization_screen):
        if last_level == 0:
            game_name_rect = game_name.get_rect(center=(SCREEN_WIDTH/2, 80))
            myScreen.blit(game_name, game_name_rect)
        else:
            last_level_text = big_font.render(
                "LEVEL: {}".format(last_level), True, WHITE)
            last_level_rect = last_level_text.get_rect(
                center=(SCREEN_WIDTH/2, 80))
            myScreen.blit(last_level_text, last_level_rect)

    # back button
    if customization_screen or leaderboard:
        back_rect = pygame.draw.rect(myScreen, DARK_RED, [
            SCREEN_WIDTH/6-80, SCREEN_HEIGHT/6-70, 80, 40])
        back_text = smallest_font.render('BACK', True, BLACK)

        if back_rect.collidepoint(mouse_pos):
            back_text = smallest_font.render('BACK', True, WHITE)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        myScreen.blit(back_text, (SCREEN_WIDTH /
                      6-80, SCREEN_HEIGHT/6-60))
    if customization_screen:

        pygame.draw.rect(myScreen, BLACK, [SCREEN_WIDTH/4-20, 80, 340, 45])
        customize_name = big_font.render('CHANGE TARGET', True, WHITE)
        customize_name_rect = customize_name.get_rect(
            center=(SCREEN_WIDTH/2, 90))
        myScreen.blit(customize_name, customize_name_rect)

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
        # print(option_1,option_2)
        if option_1 or option_2:
            if option_2:
                pygame.draw.rect(myScreen, WHITE, [
                    SCREEN_WIDTH/2+100, SCREEN_HEIGHT-150, 140, 40])
                myScreen.blit(
                    choose_text, (SCREEN_WIDTH/2+100, SCREEN_HEIGHT-140))
            else:
                pygame.draw.rect(myScreen, DARK_RED, [
                    SCREEN_WIDTH/2+100, SCREEN_HEIGHT-150, 140, 40])
                myScreen.blit(
                    choose_text, (SCREEN_WIDTH/2+100, SCREEN_HEIGHT-140))
            if option_1:
                pygame.draw.rect(myScreen, WHITE, [
                    SCREEN_WIDTH/4-60, SCREEN_HEIGHT-150, 140, 40])
                myScreen.blit(
                    choose_text, (SCREEN_WIDTH/4-60, SCREEN_HEIGHT-140))
            else:
                pygame.draw.rect(myScreen, DARK_RED, [
                    SCREEN_WIDTH/4-60, SCREEN_HEIGHT-150, 140, 40])
                myScreen.blit(
                    choose_text, (SCREEN_WIDTH/4-60, SCREEN_HEIGHT-140))
        else:
            pygame.draw.rect(myScreen, DARK_RED, [
                SCREEN_WIDTH/2+100, SCREEN_HEIGHT-150, 140, 40])
            myScreen.blit(choose_text, (SCREEN_WIDTH/2+100, SCREEN_HEIGHT-140))

            pygame.draw.rect(myScreen, DARK_RED, [
                SCREEN_WIDTH/4-60, SCREEN_HEIGHT-150, 140, 40])
            myScreen.blit(choose_text, (SCREEN_WIDTH/4-60, SCREEN_HEIGHT-140))

    elif leaderboard:

        pygame.draw.rect(myScreen, BLACK, [SCREEN_WIDTH/4-20, 30, 340, 45])
        leader_name = big_font.render('LEADERBOARD', True, WHITE)
        leader_name_rect = leader_name.get_rect(center=(SCREEN_WIDTH/2, 55))
        myScreen.blit(leader_name, leader_name_rect)

        for i in range(0, len(score_list)):

            # only top 5
            if i == 5:
                break
            colour = BLACK
            bg_color = DARK_RED
            if(i == 0):
                colour = DARK_RED
                bg_color = GREY
            person = small_font.render(
                '{} : {}'.format(score_list[i][0], score_list[i][1]), True, colour)
            pygame.draw.rect(myScreen, bg_color, [
                             SCREEN_WIDTH/4, 160+70*i, SCREEN_WIDTH/2, 40])
            myScreen.blit(person, (SCREEN_WIDTH/3 - 40, 170+70*i))
        if len(score_list) != 0:
            myScreen.blit(knife, (SCREEN_WIDTH-200, SCREEN_HEIGHT/2-160))
        else:
            # pygame.draw.rect(myScreen, BLACK, [SCREEN_WIDTH/4-20, SCREEN_HEIGHT/2, 340, 45])
            first_line = small_font.render('WE HAVE BEEN WAITING', True, WHITE)
            first_line_rect = first_line.get_rect(
                center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            myScreen.blit(first_line, first_line_rect)
            second_line = small_font.render('FOR YOU', True, WHITE)
            second_line_rect = second_line.get_rect(
                center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+60))
            myScreen.blit(second_line, second_line_rect)

    else:
        # Leaderboard button
        leader_rect = pygame.draw.rect(myScreen, DARK_RED, [
            SCREEN_WIDTH/3-20, SCREEN_HEIGHT/2-50, 240, 40])

        leader_text = small_font.render('LEADERBOARD', True, BLACK)

        if leader_rect.collidepoint(mouse_pos):
            leader_text = small_font.render('LEADERBOARD', True, WHITE)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        myScreen.blit(leader_text, (SCREEN_WIDTH/3-13, SCREEN_HEIGHT/2-40))
        # Leaderboard button

        start_rect = pygame.draw.rect(myScreen, DARK_RED, [
            SCREEN_WIDTH/3+30, SCREEN_HEIGHT/2-100, 140, 40])

        start_text = small_font.render('START', True, BLACK)

        if start_rect.collidepoint(mouse_pos):
            start_text = small_font.render('START', True, WHITE)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        myScreen.blit(start_text, (SCREEN_WIDTH/3+50, SCREEN_HEIGHT/2-90))

        customize_rect = pygame.draw.rect(myScreen, DARK_RED, [
            SCREEN_WIDTH/3, SCREEN_HEIGHT/2, 200, 40])
        customize_text = small_font.render('CUSTOMIZE', True, BLACK)

        if customize_rect.collidepoint(mouse_pos):
            customize_text = small_font.render('CUSTOMIZE', True, WHITE)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        myScreen.blit(customize_text, (SCREEN_WIDTH /
                      3+10, SCREEN_HEIGHT/2 + 10))

        # high_score_text = small_font.render(
        #     'HIGH SCORE: {}'.format(high_score), True, BLACK)
        # pygame.draw.rect(myScreen, DARK_RED, [
        #     SCREEN_WIDTH/3-30, SCREEN_HEIGHT-100, 300, 40])
        # myScreen.blit(high_score_text, (SCREEN_WIDTH/3-10, SCREEN_HEIGHT-90))

        if customize_rect.collidepoint(mouse_pos) or start_rect.collidepoint(mouse_pos) or leader_rect.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # powerups on menu
        myScreen.blit(powerup_1, (SCREEN_WIDTH/5-60, SCREEN_HEIGHT-100))
        myScreen.blit(powerup_2, (SCREEN_WIDTH/2-30, SCREEN_HEIGHT-100))
        myScreen.blit(powerup_3, (SCREEN_WIDTH-120, SCREEN_HEIGHT-100))

    return tick, image_index


def load_level(level, circle, inventory=None):

    global user_score
    global game_over
    global knife_added
    global level_color
    # if num == 1:

    myScreen.fill(level_color)

    game_over, user_score, knife_added = kA.update(
        user_score, knife_added, inventory)

    # temporary, so after level 1 we add randomness to the circle movement
    # implemented in circle.update()
    if level > 3:
        circle.show(myScreen, 1)
    else:
        circle.show(myScreen, 0)
    inventory.tick(circle)

    score_text = big_font.render(
        '{}/{}'.format(knife_added, level_goal), True, WHITE)

    level_text = small_font.render(
        'LEVEL {}'.format(level), True, WHITE)

    # pass_info_text = small_font.render(
    #     "{}/{}".format(knife_added, level_goal), True, WHITE)

    score_rect = score_text.get_rect(
        center=(SCREEN_WIDTH / 2, 80))
    myScreen.blit(score_text, score_rect)
    myScreen.blit(level_text, (30, SCREEN_HEIGHT-60))

    # pass_info_rect = pass_info_text.get_rect(
    #     right=SCREEN_WIDTH - 30, y=SCREEN_HEIGHT - 60)
    # myScreen.blit(pass_info_text, pass_info_rect)


def main():
    # Helper functions for main() function -v
    ####################################################################################
    def reset_game():
        global myScreen
        global high_score
        global kA
        global game_over
        global user_score
        global write_name
        global name_input
        global level_goal
        global knife_added
        global last_level

        nonlocal game_start
        nonlocal customization_screen
        nonlocal tick
        nonlocal start_image_index
        nonlocal level
        nonlocal last_score
        nonlocal change_music
        nonlocal music

        last_score = level
        user_score = 0
        game_start = False
        game_over = False
        write_name = False
        customization_screen = False
        knife_added = 0
        name_input = ""
        tick = 0
        last_level = level
        level = 1
        level_goal = 2
        next_goal = 2
        start_image_index = 0
        start_transition_index_1 = 178
        start_transition_index_2 = 0
        myScreen.fill((0, 0, 0))
        kA = KnivesAirbourne(myScreen, circle, level, inventory)
        knife_obj = Knife((0, 1), 10)
        kA.add(knife_obj)

    def activate_name_screen():
        global myScreen
        global game_over
        global write_name
        nonlocal change_music
        nonlocal music

        myScreen.fill((0, 0, 0))
        game_over = True
        write_name = True
    ####################################################################################
    # Helper functions for main() functions -^

    s = 'sound'
    # SCREEN_WIDTH = 600
    # SCREEN_HEIGHT = 600

    FPS = 60

    pSizeX = 30
    pSizeY = 30

    global leaderboard
    global level_color
    global myScreen
    global high_score
    global kA
    global user_score
    global knife_added
    global level_goal
    global score_list
    global rank
    global name_input
    global option_1
    global option_2
    global last_level

    myScreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

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
    level_transition = False

    tick = 0
    image_index = 1
    start_image_index = 0
    start_transition_index_1 = 178
    start_transition_index_2 = 0
    start_animation = False
    level = 0
    last_score = -1
    next_level = True
    next_goal = 2

    inventory = Inventory(myScreen)
    circle = Circle((200, 200), [300, 300],
                    pygame.math.Vector2(0, 0), 2, circle_path)

    kA = KnivesAirbourne(myScreen, circle, level, inventory)

    knife_obj = Knife((0, 1), 10)
    kA.add_wrapper(knife_obj)
    customization_screen = False

    while running:
        pygame.display.update()
        # get high score
        # with open("high_scores.txt", 'r+') as w:
        #     try:
        #         line = w.readline().split(",")
        #         high_score = int(line[1])

        #     except:
        #         high_score = 0

        if change_music:
            pygame.mixer.music.play(-1)
            change_music = False

        clock.tick(60)
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and write_name:
                if not game_start:
                    if event.key == pygame.K_BACKSPACE:
                        name_input = name_input[:-1]

                    elif event.key == pygame.K_RETURN:

                        score_list.insert(rank, (name_input, level))
                        with open("high_scores.txt", 'w') as w:
                            for i in range(0, min(10, len(score_list))):
                                tuple = score_list[i]
                                rank_i_person = "{},{}\n".format(
                                    tuple[0], tuple[1])
                                w.write(rank_i_person)
                        score_list = score_list[0: min(10, len(score_list))]
                        reset_game()

                    else:
                        name_input += event.unicode

            elif event.type == pygame.KEYDOWN and game_start:
                if event.key == pygame.K_s:
                    print("s")
                    if inventory.use_powerup(SHRINK):
                        if kA.current != None:
                            inventory.has_shrunk = True
                            dimensions = kA.current.img.get_size()
                            kA.current.scale = True
                            kA.current.img = pygame.transform.scale(
                                kA.current.img, (dimensions[0]*0.5, dimensions[1]*0.5))
                            inventory.SHRINKS = MAX_SHRINK_COUNT
                        # use powerup
                        pass
                    else:
                        # play noise indicating it can't be used
                        pass
                elif event.key == pygame.K_a:
                    # inventory.powerups[SLOWTIME]:
                    if inventory.use_powerup(SLOWTIME):
                        # use powerup
                        print("slow")
                        circle.is_slowed = True
                        circle.speed /= 3
                        pass
                    else:
                        # play noise indicating it can't be used
                        pass

            elif event.type == pygame.MOUSEBUTTONDOWN and not(write_name):
                if game_start and not(level_transition):
                    if event.button == 1:  # if left click
                        pygame.mixer.Sound.play(knife_effect)
                        if inventory.has_shrunk:
                            inventory.SHRINKS -= 1
                        kA.handle_click()

                elif SCREEN_WIDTH/3+30 <= mouse[0] <= SCREEN_WIDTH/3+170 and SCREEN_HEIGHT/2-100 <= mouse[1] <= SCREEN_HEIGHT/2-60 and not(level_transition):
                    start_animation = True

                elif SCREEN_WIDTH/3 <= mouse[0] <= SCREEN_WIDTH/3+200 and SCREEN_HEIGHT/2 <= mouse[1] <= SCREEN_HEIGHT/2+40:
                    customization_screen = True

                elif SCREEN_WIDTH/4-20 <= mouse[0] <= SCREEN_WIDTH/3+340 and SCREEN_HEIGHT/2-50 <= mouse[1] <= SCREEN_HEIGHT/2-5:
                    leaderboard = True
                elif SCREEN_WIDTH/6-80 <= mouse[0] <= SCREEN_WIDTH/6 and SCREEN_HEIGHT/6-70 <= mouse[1] <= SCREEN_HEIGHT/2-30:
                    leaderboard = False
                    customization_screen = False

                # if user chooses bowling ball
                elif SCREEN_WIDTH/2+100 <= mouse[0] <= SCREEN_WIDTH/2+240 and SCREEN_HEIGHT-150 <= mouse[1] <= SCREEN_HEIGHT-110 and customization_screen:
                    option_2 = True
                    option_1 = False
                    circle_path = circle_2_path
                    circle = Circle((200, 200), [300, 300],  pygame.math.Vector2(
                        0, 0), level+3, circle_path)
                elif SCREEN_WIDTH/4-60 <= mouse[0] <= SCREEN_WIDTH/2+80 and SCREEN_HEIGHT-150 <= mouse[1] <= SCREEN_HEIGHT-110 and customization_screen:
                    option_1 = True
                    option_2 = False
                    circle_path = circle_1_path
                    circle = Circle((200, 200), [300, 300],  pygame.math.Vector2(
                        0, 0), level+3, circle_path)

        # If asking for user input for new high score
        if write_name:
            tick, image_index = insert_name(tick, image_index, myScreen, level)

        # Playing game part
        elif game_start and not(start_animation):

            if knife_added >= level_goal and next_level:
                level_transition = True

                if level_transition:
                    inventory.has_shrunk = False
                    inventory.SHRUNK = MAX_SHRINK_COUNT
                    if level_color == DARK_RED:
                        start_transition_index_1 += 1

                        # coz there are 150 pictures for that animation, we wanna stop once we are done with them
                        if start_transition_index_1 > 336:
                            level_transition = False
                            start_transition_index_1 = 178

                        transition = pygame.image.load(
                            "resources/start_animation/frame_{:03d}_delay-0.03s.gif".format(start_transition_index_1)).convert_alpha()
                        transition = pygame.transform.scale(
                            transition, (600, 600))
                        myScreen.blit(transition, (0, 0))
                    else:
                        start_transition_index_2 += 1

                        # coz there are 150 pictures for that animation, we wanna stop once we are done with them
                        if start_transition_index_2 > 150:
                            level_transition = False
                            start_transition_index_2 = 0

                        transition = pygame.image.load(
                            "resources/start_animation/frame_{:03d}_delay-0.03s.gif".format(start_transition_index_2)).convert_alpha()
                        transition = pygame.transform.scale(
                            transition, (600, 600))
                        myScreen.blit(transition, (0, 0))

                if not(level_transition):
                    if level_color == DARK_RED:
                        level_color = NEW_BLACK
                    else:
                        level_color = DARK_RED
                    level += 1
                    user_score = 0
                    # next level music
                    # mp3_name = "sound_" + str(random.randint(1, 2)) + ".mp3"
                    # pygame.mixer.music.load(os.path.join(s, mp3_name))
                    # change_music = True

                    # this is to reset everything and add new knives and circle
                    circle = Circle((200, 200), [300, 300],  pygame.math.Vector2(
                        0, 0), level+1, circle_path)
                    kA = KnivesAirbourne(myScreen, circle, level, inventory)
                    knife_obj = Knife((0, 1), 10)
                    kA.add_wrapper((knife_obj))
                    next_level = True
                    level_goal = min(level + 1, 50)
                    next_goal += level_goal
                    knife_added = 0

                # continue coz we need to get rid of the old stuff by sending it to the pygame.update line
                # with this continue keyword
                continue
            load_level(level, circle, inventory)
            inventory.update()

            # load_level(level, circle)

            # resets game
            # resets game
            if game_over:
                pygame.mixer.music.load(os.path.join(s, 'game_over.mp3'))
                change_music = True
                game_start = False
                last_level = level
                # Check if potential highscore
                inventory.reset()
                if len(score_list) == 0:
                    rank = 0
                    activate_name_screen()

                elif len(score_list) == 1:
                    if score_list[0][1] >= level:
                        rank = 1
                    else:
                        rank = 0
                    activate_name_screen()

                elif len(score_list) > 1:
                    found_rank = False
                    if score_list[0][1] <= level:
                        rank = 0
                    else:
                        for i in range(1, min(9, len(score_list)-1)):
                            if(level <= score_list[i][1] and level >= score_list[i+1][1]):
                                rank = i+1
                                found_rank = True
                                break
                            else:
                                rank = 11

                    if(len(score_list) == 10 and score_list[-1][1] == level):
                        reset_game()

                    elif rank <= 9:
                        activate_name_screen()

                    elif(len(score_list) < 10 and not(found_rank)):
                        rank = len(score_list)
                        activate_name_screen()

                    else:
                        reset_game()

        else:
            tick, image_index = menu_screen(
                tick, image_index, myScreen, customization_screen, leaderboard, last_level)

            if start_animation:

                start_image_index += 1

                # coz there are 150 pictures for that animation, we wanna stop once we are done with them
                if start_image_index > 150:
                    start_animation = False
                    game_start = True
                    change_music = True
                    mp3_name = "sound_" + str(random.randint(1, 2)) + ".mp3"
                    music = pygame.mixer.music.load(
                        os.path.join(s, mp3_name))
                transition = pygame.image.load(
                    "resources/start_animation/frame_{:03d}_delay-0.03s.gif".format(start_image_index)).convert_alpha()
                transition = pygame.transform.scale(transition, (600, 600))
                myScreen.blit(transition, (0, 0))
                level = 1
        tick += 1
     # pygame.display.flip()


if __name__ == '__main__':
    # Load score list
    with open("high_scores.txt", 'r') as hs:
        for line in hs.readlines():
            cur_line = line.strip().rsplit(',', 1)
            score_list.append((cur_line[0], int(cur_line[1])))
    main()
