from pygame import *
from knife import SLOWTIME,SHRINK,EXTRALIFE


class Inventory:
    def __init__(self,screen):
        self.apples = 0
        self.screen = screen
        self.powerups = [False for x in range(3)]

    def update(self):
        return

    def add_powerup(self,index):
        print(f"added {index}")
        self.powerups[index] = True
    
    def use_powerup(self,index):
        if self.powerups[index]:
            self.powerups[index] = False
            return True
        return False
    
    def increment_currency(self):
        self.apples += 1