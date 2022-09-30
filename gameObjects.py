import pygame
from pygame.locals import *

class Vector:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

class Knife(pygame.sprite.Sprite):
    def __init__(self, direction,speed):
        pygame.sprite.Sprite.__init__(self)
        self.direction = Vector(direction)

        knife = pygame.image.load("./sword.png").convert_alpha()
        dimensions = knife.get_size()
        knife = pygame.transform.scale(knife, (dimensions[0]/8,dimensions[1]/8))
        self.img  = pygame.transform.rotate(knife,180)

        self.speed = speed
        self.location = (290,500)

    def move_knife(self,screen):
        new_pos = (self.location[0] - self.speed * self.direction.x,self.location[1] - self.speed * self.direction.y)
        screen.blit(self.img, new_pos)
        self.location = new_pos

class KnivesAirbourne(pygame.sprite.Group):
    def __init__(self,screen):
        pygame.sprite.Group.__init__(self)
        self.screen = screen

    def update(self):
        for entities in self.sprites():
            entities.move_knife(self.screen)