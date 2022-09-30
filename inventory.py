from pygame import *

SLOWTIME = 0
SHRINK = 1


class Inventory:
    def __init__(self, number_knives, inventory):
        self.number_knives = number_knives
        self.powerups = [False for x in range(2)]

    def add_powerup(self, powerup,index):
        self.powerups[index] = True
    
    def use_powerup(self, powerup,index):
        if self.powerups[index]:
            self.powerups[index] = False
            return True
        return False

    def use_knife(self):
        if self.number_knives > 0:
            self.number_knives -=1
            return True
        return False

    def set_knives(self,knives):
        self.number_knives = knives