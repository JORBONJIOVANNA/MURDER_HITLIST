import pygame
from regex import W


class Orb(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int]):
        super().__init__()
        self.position = position

        img = pygame.image.load("./orb.png").convert_alpha()
        self.img = pygame.transform.scale(img, (150, 150))

        self.rect = self.img.get_rect()

        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.angle = 0

    def update(self):
        self.angle = (self.angle + 2) % 360
        self.img = pygame.transform.rotate(self.img, self.angle)

    def draw(self, screen):
        self.update()
        screen.blit(self.img, self.position)
