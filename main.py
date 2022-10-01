
import pygame
from pygame.locals import *
from circle import Circle
from knife import *
import os
import inventory
import random

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
LIGHT_GREY = (60, 60, 60)
DARK_RED = (107, 0, 0)
BLACK = (0, 0, 0)

high_score = 0
user_score = 0
game_over = False

score_list = []
rank = 11
name_input = ''
write_name = False

smallest_font = pygame.font.SysFont('Cooper	', 30)
small_font = pygame.font.SysFont('Verdana', 30)
big_font = pygame.font.SysFont('Verdana', 45)
game_name = big_font.render('KNIFE HIT', True, LIGHT_GREY)
start_text = small_font.render('START', True, BLACK)

def menu_screen(tick, image_index, myScreen, last_score=-1):
    if tick%6 == 5:
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
        myScreen.blit(game_name, (SCREEN_WIDTH/4+30, SCREEN_HEIGHT/4-90))
    else:
        last_score_text = big_font.render(
            "PREVIOUS SCORE: {}".format(last_score), True, LIGHT_GREY)
        myScreen.blit(last_score_text, (SCREEN_WIDTH/10+30, SCREEN_HEIGHT/4-90))

    pygame.draw.rect(myScreen, DARK_RED, [
                     SCREEN_WIDTH/3+30, SCREEN_HEIGHT/2-100, 140, 40])
    myScreen.blit(start_text, (SCREEN_WIDTH/3+50, SCREEN_HEIGHT/2-100))

    high_score_text = small_font.render(
        'HIGH SCORE: {}'.format(high_score), True, BLACK)
    pygame.draw.rect(myScreen, DARK_RED, [
                     SCREEN_WIDTH/3-30, SCREEN_HEIGHT-100, 300, 40])
    myScreen.blit(high_score_text, (SCREEN_WIDTH/3-10, SCREEN_HEIGHT-100))
    return tick, image_index

#When game asks for user input
def insert_name(tick, image_index, myScreen, level):
    global name_input
    global rank
    
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

    success_message_1 = smallest_font.render('Well done Murderer! You reached level {} which is rank {}!'.format(level, rank+1), True, WHITE)
    success_message_2 = smallest_font.render('Please enter your name to go on Serial Killer List', True, WHITE)
    myScreen.blit(success_message_1, (15, SCREEN_HEIGHT/3-60))
    myScreen.blit(success_message_2, (50, SCREEN_HEIGHT/3-40))

    pygame.draw.rect(myScreen, DARK_RED, [SCREEN_WIDTH/4, SCREEN_HEIGHT/2-100, SCREEN_WIDTH/2, 40])

    if(pygame.time.get_ticks()%1000 < 500):
        name_output = smallest_font.render(name_input, True, WHITE)
    else:
        name_output = smallest_font.render(name_input + "|", True, WHITE)
    
    myScreen.blit(name_output, (SCREEN_WIDTH/4+10, SCREEN_HEIGHT/3+10))

    return tick, image_index


def load_level(level,circle):
    
    global user_score
    global game_over

    # if num == 1:
    
    myScreen.fill(DARK_RED)

    game_over, user_score = kA.update(user_score)

    # temporary, so after level 1 we add randomness to the circle movement
    # implemented in circle.update()
    if level > 1:
        circle.show(myScreen,1)
    else:
        circle.show(myScreen,0)
    
    target_text = small_font.render(
    'LEFT: {}'.format(circle.num - user_score), True, WHITE)
    myScreen.blit(target_text, (SCREEN_WIDTH/3+25, SCREEN_HEIGHT/4-50))

    score_text = small_font.render(
    'SCORE: {}'.format(user_score), True, WHITE)

    level_text = small_font.render(
    'LEVEL {}'.format(level), True, WHITE)
    myScreen.blit(score_text, (SCREEN_WIDTH/3+20, SCREEN_HEIGHT/4-100))
    myScreen.blit(level_text, (SCREEN_WIDTH/5-60, SCREEN_HEIGHT-60))

def main():
    #Helper functions for main() functions
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
        name_input = ""
        tick = 0
        level = 1
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
    global rank
    global score_list
    global write_name
    global name_input

    myScreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("KNIFE HIT")

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

    circle = Circle((200, 200), [300, 300],  pygame.math.Vector2(0, 0),2)

    kA = KnivesAirbourne(myScreen, circle,level)
    knife_obj = Knife((0, 1), 10)
    kA.add(knife_obj)

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

            elif event.type == pygame.KEYDOWN and game_start:

                if event.key == pygame.K_UP:
                    circle.increase_speed()
                if event.key == pygame.K_DOWN:
                    circle.decrease_speed()

        # Playing Game part
        if game_start and not(start_animation) and not(write_name):
            if user_score == circle.num and next_level:
                level += 1
                user_score = 0
                #next level music
                mp3_name = "sound_" + str(random.randint(1, 2)) + ".mp3"
                pygame.mixer.music.load(os.path.join(s, mp3_name))
                change_music = True

                # this is to reset everything and add new knives and circle
                circle = Circle((200, 200), [300, 300],  pygame.math.Vector2(0, 0), level+3)
                kA = KnivesAirbourne(myScreen, circle,level)
                knife_obj = Knife((0, 1), 10)
                kA.add(knife_obj)
                next_level = True
                # continue coz we need to get rid of the old stuff by sending it to the pygame.update line
                # with this continue keyword
                continue

            load_level(level,circle)

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
                    for i in range(0, min(9, len(score_list)-1)):
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
                tick, image_index, myScreen, last_score)

            if start_animation:
                
                start_image_index += 1

                #coz there are 150 pictures for that animation, we wanna stop once we are done with them
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
    print(score_list)
    main()
