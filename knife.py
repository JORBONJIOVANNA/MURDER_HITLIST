import pygame
from pygame.locals import *

import random

from utils import rotate

RESTING = 0
MOVING = 1
STUCK = 2


class Vector:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]


class Knife(pygame.sprite.Sprite):
    def __init__(self, direction, speed):
        pygame.sprite.Sprite.__init__(self)
        self.direction = Vector(direction)

        knife = pygame.image.load("resources/sword.png").convert_alpha()
        dimensions = knife.get_size()
        knife = pygame.transform.scale(
            knife, (dimensions[0]/8, dimensions[1]/8))
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
            new_img, new_rect = rotate(
                self.img, self.stuck_angle, circle.pivot, pygame.math.Vector2(0, 140))
            screen.blit(new_img, new_rect)
            self.rotated_rect = new_rect
            # print(new_rect)
            return

        if self.location[1] != self.shoot_location[1]:
            self.move_knife()

        screen.blit(self.img, self.location)


class KnivesAirbourne(pygame.sprite.Group):
    def __init__(self, screen, circle, level):
        pygame.sprite.Group.__init__(self)
        self.screen = screen
        self.circle = circle
        number_knives = level
        for x in range(number_knives):
            knife = Knife((0, 0), 0)
            knife.state = STUCK
            knife.stuck_angle = random.randrange(0, 360, 10)
            self.add(knife)

    def check_collision(self, knife):
        for entity in self.sprites():
            if entity.state == STUCK and entity != knife:

                # checks collision
                if 275 <= entity.rotated_rect.x <= 305 and 370 <= entity.rotated_rect.y <= 400:
                    return -1
                # return 0

    def handle_click(self):
        for entity in self.sprites():
            if entity.state == RESTING:
                entity.state = MOVING

    def update(self, score, knife_added):
        game_over = False
        add_new = True
        is_all_moved = True

        for entity in self.sprites():
            # entity.move_knife()
            entity.show(self.screen, self.circle)

            if entity.location[1] > 0 and entity.state != STUCK:
                add_new = False

            if entity.location[1] < 400 and entity.state == MOVING:
                entity.state = STUCK
                entity.stuck_angle = 0
                if self.check_collision(entity) == -1:
                    game_over = True
                else:
                    game_over = False
                    score += 1
                    knife_added += 1

        for entity in self.sprites():
            if entity.state == RESTING:
                is_all_moved = False
                break

        if add_new and is_all_moved:
            self.add(Knife((0, 1), 10))

        return game_over, score, knife_added
