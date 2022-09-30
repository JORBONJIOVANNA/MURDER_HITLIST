import pygame
from regex import W


class Circle(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], pivot, offset):
        super().__init__()
        self.position = position

        img = pygame.image.load("circle.png").convert_alpha()
        self.img = pygame.transform.scale(img, (200, 200))

        self.rect = self.img.get_rect()

        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.angle = 0
        self.speed = 2
        self.pivot = pivot
        self.offset = offset

    def increase_speed(self):
        self.speed = min(12, self.speed + 2)

    def decrease_speed(self):
        self.speed = max(2, self.speed - 2)

    def rotate(self):
        # Rotate the image.
        rotated_image = pygame.transform.rotozoom(self.img, -self.angle, 1)
        # Rotate the offset vector.
        rotated_offset = self.offset.rotate(self.angle)
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=self.pivot+rotated_offset)
        # Return the rotated image and shifted rect.
        return rotated_image, rect

    def update(self):
        self.angle += self.speed

    def show(self, screen):
        self.update()
        img, rect = self.rotate()
        screen.blit(img, rect)
