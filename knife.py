import pygame
from pygame.locals import *

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

        self.speed = speed
        self.location = (290, 500)
        self.state = RESTING
        self.stuck_angle = 0

    def move_knife(self):
        new_pos = (self.location[0] - self.speed * self.direction.x,
                   self.location[1] - self.speed * self.direction.y)
        # screen.blit(self.img, new_pos)
        self.location = new_pos

    def show(self, screen, circle):
        if self.state == MOVING:
            self.move_knife()

        if self.state == STUCK:
            self.stuck_angle += circle.speed
            new_img, new_rect = rotate(
                self.img, self.stuck_angle, circle.pivot, pygame.math.Vector2(0, 100))
            screen.blit(new_img, new_rect)
            return

        screen.blit(self.img, self.location)


class KnivesAirbourne(pygame.sprite.Group):
    def __init__(self, screen, circle):
        pygame.sprite.Group.__init__(self)
        self.screen = screen
        self.circle = circle

    def handle_click(self):
        for entity in self.sprites():
            if entity.state == RESTING:
                entity.state = MOVING

    def update(self):
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

        for entity in self.sprites():
            if entity.state == RESTING:
                is_all_moved = False
                break

        if add_new and is_all_moved:
            self.add(Knife((0, 1), 10))
            print("Added new knife")
