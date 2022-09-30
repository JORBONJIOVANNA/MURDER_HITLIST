
import pygame
from pygame.locals import *


def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

class Vector:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

class Circle(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        
        self.circle = pygame.image.load("./circle.png").convert_alpha()
        self.circle = pygame.transform.scale(self.circle, (200,200))
        self.screen = screen
        self.speed = 2
        self.location = (300,300)
        self.pivot = [300, 300]
        self.offset = pygame.math.Vector2(0, 0)
        self.angle = 0

    def rotate_circle(self):
        self.angle += self.speed
        rotated_image, rect = rotate(self.circle, self.angle, self.pivot, self.offset)
        self.screen.blit(rotated_image, rect)
    
    def change_speed(self,speed):
        self.speed = speed

class Knife(pygame.sprite.Sprite):
    def __init__(self, direction,speed):
        pygame.sprite.Sprite.__init__(self)
        self.direction = Vector(direction)

        knife = pygame.image.load("./sword.png").convert_alpha()
        dimensions = knife.get_size()
        knife = pygame.transform.scale(knife, (dimensions[0]/8,dimensions[1]/8))
        self.img  = pygame.transform.rotate(knife,180)

        self.speed = speed
        self.location = (300,300)

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