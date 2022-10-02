import pygame
from pygame.locals import *

import random

from utils import *

RESTING = 0
MOVING = 1
STUCK = 2

SLOWTIME = 0
SLOWTIME_DURATION = 4000
SHRINK = 1
MAX_SHRINK_COUNT = 3
EXTRALIFE =2

EXTRALIFE_PERCENTAGE = 5
SLOWTIME_PERCENTAGE = 35
SHRINK_PERCENTAGE = 35


class Vector:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]


class Knife(pygame.sprite.Sprite):
    def __init__(self, direction, speed,scale=False):
        pygame.sprite.Sprite.__init__(self)
        self.direction = Vector(direction)

        knife = pygame.image.load("resources/sword.png").convert_alpha()
        dimensions = knife.get_size()
        self.scale = scale
        scaling = 8 if not scale else 16
        knife = pygame.transform.scale(
            knife, (dimensions[0]/scaling, dimensions[1]/scaling))
        self.img = pygame.transform.rotate(knife, 180)
        self.rect = self.img.get_rect()
        self.rotated_rect = None

        self.speed = speed
        self.location = (290, 600)
        self.shoot_location = (290, 500)

        self.state = RESTING
        self.stuck_angle = 0

    def move_knife(self):
        new_pos = (self.location[0] - self.speed * self.direction.x,
                   self.location[1] - self.speed * self.direction.y)
        # screen.blit(self.img, new_pos)
        self.location = new_pos
        self.rect.x = new_pos[0]
        self.rect.y = new_pos[1]

    def show(self, screen, circle):
        if self.state == MOVING:
            self.move_knife()
            # print(self.rect.y)

        if self.state == STUCK:
            self.rect.y = 400
            self.stuck_angle += circle.speed
            offset = 140 if not self.scale else 120
            new_img, new_rect = rotate(
                self.img, self.stuck_angle, circle.pivot, pygame.math.Vector2(0, offset))
            screen.blit(new_img, new_rect)
            self.rotated_rect = new_rect
            return

        if self.location[1] != self.shoot_location[1]:
            self.move_knife()

        screen.blit(self.img, self.location)


class Powerup(pygame.sprite.Sprite):
    def __init__(self, id):
        pygame.sprite.Sprite.__init__(self)
        self.power = id
        self.power_time = 7.5
        self.angle = 0
        img = None
        if id == SLOWTIME:
            img = pygame.image.load(
                "resources/game_icons/slow_menu.png").convert_alpha()
        elif id == SHRINK:
            img = pygame.image.load(
                "resources/game_icons/shrink_menu.png").convert_alpha()
        elif id == EXTRALIFE:
            img = pygame.image.load(
                "resources/game_icons/extra_active.png").convert_alpha()
        else:
            self.img = None
            self.rect = None
            self.rotated_rect = None
            return

        dimensions = img.get_size()
        img = pygame.transform.scale(
            img, (dimensions[0]*0.5, dimensions[1]*0.5))

        self.img = pygame.transform.rotate(img, 180)
        self.rect = self.img.get_rect()
        self.rotated_rect = None
        ""'level powerups?'""
        # self.power_level = 1

    def show(self, screen, circle):
        self.rect.y = 400
        self.angle += circle.speed
        new_img, new_rect = rotate(
            self.img, self.angle, circle.pivot, pygame.math.Vector2(0, 115))
        screen.blit(new_img, new_rect)
        self.rotated_rect = new_rect


class KnivesAirbourne(pygame.sprite.Group):

    def generate_knives(self, number_knives):
        angles = []
        for x in range(number_knives):
            knife = Knife((0, 0), 0)
            knife.state = STUCK
            rand_angle = random.randrange(0, 360, 30)
            knife.stuck_angle = rand_angle
            angles.append(rand_angle)
            self.add(knife)
        return angles

    def generate_powerups(self, angles,inventory):
        chance = random.randrange(0, 100)
        y = 0
        for x in [EXTRALIFE_PERCENTAGE, SLOWTIME_PERCENTAGE,SHRINK_PERCENTAGE]:
            if chance < x:
                if inventory.powerups[y] == True:
                    continue
                obj = Powerup(y)

                while(True):
                    rand_angle = random.randrange(0, 360, 15)
                    if checkifdistance(angles, rand_angle, 15):
                        break
                obj.angle = rand_angle
                angles.append(rand_angle)
                self.add(obj)
                break
                # y+=1
            chance = random.randrange(0, 100)
            y +=1

    def __init__(self, screen, circle, level,inventory):
        pygame.sprite.Group.__init__(self)
        self.screen = screen
        self.circle = circle
        position = self.generate_knives(level)
        self.generate_powerups(position,inventory)
        self.current = None


    def check_collision(self, knife):
        for entity in self.sprites():
            if type(entity) is Powerup:
                print(entity.power,entity.rotated_rect.x, entity.rotated_rect.y)
                # if 275 <= entity.rotated_rect.x <= 305 and 370 <= entity.rotated_rect.y <= 400:
                if 275 <= entity.rotated_rect.x <= 315 and 370 <= entity.rotated_rect.y <= 405:
                    return 0,entity
            else:
                if entity.state == STUCK and entity != knife:

                    # checks collision
                    if 275 <= entity.rotated_rect.x <= 305 and 370 <= entity.rotated_rect.y <= 405:
                        return -1,entity
                    # return 0
        return 1, None

    def handle_click(self):
        for entity in self.sprites():
            if type(entity) is Powerup:
                continue
            if entity.state == RESTING:
                entity.state = MOVING

    def add_wrapper(self,sprite):
        self.current = sprite
        self.add(sprite)

    def update(self, score, knife_added, inventory=None):
        game_over = False
        add_new = True
        is_all_moved = True

        deleted = None

        for entity in self.sprites():
            # entity.move_knife()
            entity.show(self.screen, self.circle)

            if type(entity) is Powerup:
                continue

            if entity.location[1] > 0 and entity.state != STUCK:
                add_new = False

            if entity.location[1] < 400 and entity.state == MOVING:
                entity.state = STUCK
                entity.stuck_angle = 0
                collision_id, collision = self.check_collision(entity)
                if collision_id == -1:
                    if (inventory is None):
                        game_over = True
                    else:
                        if not inventory.use_powerup(EXTRALIFE):
                            game_over = True
                        else:
                            deleted = collision
                else:
                    if isinstance(collision, Powerup):
                        inventory.add_powerup(collision.power)
                        deleted = collision
                        self.remove(deleted)
                    else:
                        game_over = False
                    score += 1
                    knife_added += 1

        # self.remove(deleted)

        for entity in self.sprites():
            if type(entity) is Powerup:
                continue
            if entity.state == RESTING:
                is_all_moved = False
                break

        if add_new and is_all_moved:
            self.add_wrapper(Knife((0, 1), 10, inventory.has_shrunk and inventory.SHRINKS >0))

        return game_over, score, knife_added
# Make the game score as how many levels beat
# When a level is over to load next level
# Top 10 scores <- good
