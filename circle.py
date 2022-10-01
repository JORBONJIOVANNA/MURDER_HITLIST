import pygame
import random as rd

class Circle(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], pivot, offset,speed,path):
        super().__init__()
        self.position = position

        img = pygame.image.load("resources/{}".format(path)).convert_alpha()
        self.img = pygame.transform.scale(img, (200, 200))

        self.rect = self.img.get_rect()

        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.is_slowed = False

        self.raw_speed = speed

        self.angle = 0
        self.switch = 0
        self.last_angle = 0
        lower_bound = max(1,speed)
        self.speed = rd.randint(lower_bound, speed%12)+1
        self.num = rd.randint(0, speed%10)+3
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

    def update(self,random):
        speeds = [-2,2,4]
        if random:
            
            # changes after it rotates 60 degrees
            if self.switch > 60:
                self.switch = 0
                index = rd.randint(0,2)
                self.speed = speeds[index]
            if not self.is_slowed:
                self.angle += self.speed
            self.switch += abs(self.speed)
        else:
            if not self.is_slowed:
                self.angle += self.speed

    def show(self, screen,random):
        
        self.update(random)
        img, rect = self.rotate()
        screen.blit(img, rect)
