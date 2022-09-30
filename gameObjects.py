class Vector:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

class Knife:
    def __init__(self, direction,img,speed):
        self.direction = Vector(direction)
        self.img =img
        self.speed = speed
        self.location = (225,500)

    def move_knife(self,screen):
        new_pos = (self.location[0] - self.speed * self.direction.x,self.location[1] - self.speed * self.direction.y)
        screen.blit(self.img, new_pos)
        self.location = new_pos

