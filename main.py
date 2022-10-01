import pygame
from pygame.locals import *
from circle import Circle
from knife import *
import os
<<<<<<< HEAD
from inventory import *

=======
import inventory
import random
>>>>>>> origin/HrudayAlistairMerge

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
score_list = []
rank = 11
name_input = ''
write_name = False

circle_1_path = "circle.png"
circle_2_path = "circle_2.png"

circle_1 = pygame.image.load(
    "resources/{}".format(circle_1_path)).convert_alpha()
circle_1 = pygame.transform.scale(circle_1, (100, 100))

circle_2 = pygame.image.load(
    "resources/{}".format(circle_2_path)).convert_alpha()
circle_2 = pygame.transform.scale(circle_2, (100, 100))

smallest_font = pygame.font.Font('fonts/PPEditorialNew-Ultralight.otf', 27)
small_font = pygame.font.Font('fonts/PPEditorialNew-Ultralight.otf', 30)
big_font = pygame.font.Font('fonts/PPEditorialNew-Ultralight.otf', 45)
game_name = big_font.render('KNIFE HIT', True, WHITE)

start_text = small_font.render('START', True, BLACK)
customize_text = small_font.render('CUSTOMIZE', True, BLACK)
choose_text = small_font.render('CHOOSE', True, BLACK)

#When game asks for user input, this is purely rendering the screen
def insert_name(tick, image_index, myScreen, level):
    global name_input
    global rank
    global smallest_font
    global SCREEN_HEIGHT
    global SCREEN_WIDTH

    #Rendering    
    if tick%6 == 5:
        tick = 0
        image_index += 1
        if image_index > 11:
            image_index = 1
        menu_img = pygame.image.load(
            "resources/menu_images/frame_{}.gif".format(image_index)).convert_alpha()
        menu_img = pygame.transform.scale(menu_img, (600, 600))
        myScreen.blit(menu_img, (0, 0))

    success_message_1 = smallest_font.render('Well done Murderer!', True, WHITE)
    success_message_2 = smallest_font.render('You reached level {} which is rank {}!'.format(level, rank+1), True, WHITE)
    success_message_3 = smallest_font.render('Please enter your name to go on Serial Killer List:', True, WHITE)
    myScreen.blit(success_message_1, (SCREEN_WIDTH/3 - 20, SCREEN_HEIGHT/3-100))
    myScreen.blit(success_message_2, (SCREEN_HEIGHT/4 - 30, SCREEN_HEIGHT/3-70))
    myScreen.blit(success_message_3, (50, SCREEN_HEIGHT/3-40))

    pygame.draw.rect(myScreen, DARK_RED, [SCREEN_WIDTH/4, SCREEN_HEIGHT/2-100, SCREEN_WIDTH/2, 40])

    if(pygame.time.get_ticks()%1000 < 500):
        name_output = smallest_font.render(name_input, True, WHITE)
    else:
        name_output = smallest_font.render(name_input + "|", True, WHITE)
    
    myScreen.blit(name_output, (SCREEN_WIDTH/4+5, SCREEN_HEIGHT/3+5))

    return tick, image_index


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

def load_level(level,circle,inventory):
    
    global user_score
    global game_over
    global knife_added

    # if num == 1:

    myScreen.fill(DARK_RED)

    game_over, user_score, knife_added = kA.update(user_score, knife_added,inventory)

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
    #Helper functions for main() function -v
    ####################################################################################
    def reset_game():
        global myScreen
        global high_score
        global kA
        global game_over
        global user_score
        global write_name
        global name_input

        nonlocal game_start
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
        knife_added = 0
        name_input = ""
        tick = 0
        level = 1
        level_goal = 2
        next_goal = 2
        start_image_index = 0
        myScreen.fill((0, 0, 0))
        kA = KnivesAirbourne(myScreen, circle,level)
        knife_obj = Knife((0, 1), 10)
        kA.add(knife_obj)
        change_music = True
        music = pygame.mixer.music.load(os.path.join(s, 'menu.mp3'))

    def activate_name_screen():
        global myScreen
        global game_over
        global write_name
        nonlocal change_music
        nonlocal music

        myScreen.fill((0, 0, 0))
        change_music = True
        game_over = True
        music = pygame.mixer.music.load(os.path.join(s, 'menu.mp3'))
        write_name = True
    ####################################################################################
    #Helper functions for main() functions -^

    s = 'sound'
    # SCREEN_WIDTH = 600
    # SCREEN_HEIGHT = 600

    FPS = 60

    pSizeX = 30
    pSizeY = 30

    global myScreen
    global high_score
    global kA
    global user_score
    global knife_added
    global level_goal
    global score_list
    global rank
    global name_input
    
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

    kA = KnivesAirbourne(myScreen, circle,level)
    inventory = Inventory(myScreen)
    knife_obj = Knife((0, 1), 10)
    kA.add(knife_obj)
    customization_screen = False

    while running:
        pygame.display.update()
        # get high score
        with open("high_scores.txt", 'r+') as w:
            try:
                line = w.readline().split(",")
                high_score = int(line[1])
            
            except:
                high_score = 0

        if change_music:
            pygame.mixer.music.play(-1)
            change_music = False

        clock.tick(60)
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and write_name:
                if event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]

                elif event.key == pygame.K_RETURN:

                    score_list.insert(rank, (name_input, level))
                    with open("high_scores.txt", 'w') as w:
                        for i in range(0, min(10, len(score_list))):
                            tuple = score_list[i]
                            rank_i_person = "{},{}\n".format(tuple[0], tuple[1])
                            w.write(rank_i_person)
                    score_list = score_list[0 : min(10, len(score_list))]
                    reset_game()

                else:
                    name_input += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN and not(write_name):
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

        #Playing game part
        if game_start and not(start_animation) and not(write_name):

            if knife_added >= level_goal and next_level:
                level += 1
                user_score = 0
                #next level music
                mp3_name = "sound_" + str(random.randint(1, 2)) + ".mp3"
                pygame.mixer.music.load(os.path.join(s, mp3_name))
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
            load_level(level,circle,inventory)
            inventory.update()

            # resets game
            # resets game
            if game_over:
                #Check if potential highscore
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
        #If asking for user input for new high score
        elif write_name:
            tick, image_index = insert_name(tick, image_index, myScreen, level)

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
                    mp3_name = "sound_" + str(random.randint(1, 2)) + ".mp3"
                    music = pygame.mixer.music.load(
                        os.path.join(s, mp3_name))
                transition = pygame.image.load(
                    "resources/start_animation/frame_{:03d}_delay-0.03s.gif".format(start_image_index)).convert_alpha()
                transition = pygame.transform.scale(transition, (600, 600))
                myScreen.blit(transition, (0, 0))
        tick += 1
     # pygame.display.flip()


if __name__ == '__main__':
    #Load score list
    with open("high_scores.txt", 'r') as hs:
        for line in hs.readlines():
            cur_line = line.strip().split(",")
            score_list.append((cur_line[0], int(cur_line[1])))
    main()