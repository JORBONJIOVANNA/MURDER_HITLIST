from knife import SLOWTIME, SHRINK, EXTRALIFE
import pygame


class Inventory:
    def resize_img(self, img, scale=8):
        dimensions = img.get_size()
        img = pygame.transform.scale(
            img, (dimensions[0]/scale, dimensions[1]/scale))
        return img

    def __init__(self, screen):
        self.apples = 0
        self.screen = screen
        self.powerups = [False for x in range(3)]
        slow_img_inactive = pygame.image.load(
            "resources/game_icons/slow_inactive.png").convert_alpha()

        # slow_img_inactive = self.resize_img(slow_img_inactive)
        slow_img_active = pygame.image.load(
            "resources/game_icons/slow_active.png").convert_alpha()
        # slow_img_active = self.resize_img(slow_img_active)

        shrink_img_inactive = pygame.image.load(
            "resources/game_icons/shrink_inactive.png").convert_alpha()
        # shrink_img_inactive = self.resize_img(shrink_img_inactive,16)
        shrink_img_active = pygame.image.load(
            "resources/game_icons/shrink_active.png").convert_alpha()
        # shrink_img_active = self.resize_img(shrink_img_active,16)

        extral_img_inactive = pygame.image.load(
            "resources/game_icons/extra_inactive.png").convert_alpha()
        # extral_img_inactive = self.resize_img(extral_img_inactive,16)

        extral_img_active = pygame.image.load(
            "resources/game_icons/extra_active.png").convert_alpha()
        # extral_img_active = self.resize_img(extral_img_active,16)

        self.img = [(slow_img_active, slow_img_inactive), (shrink_img_active,
                                                           shrink_img_inactive), (extral_img_active, extral_img_inactive)]

    def update(self):
        for x in range(3):
            self.screen.blit(
                self.img[x][0] if self.powerups[x] else self.img[x][1],
                (420+50*x, 525)
            )

    def add_powerup(self, index):
        print(f"added {index}")
        self.powerups[index] = True

    def use_powerup(self, index):
        if self.powerups[index]:
            self.powerups[index] = False
            return True
        return False

    def increment_currency(self):
        self.apples += 1
