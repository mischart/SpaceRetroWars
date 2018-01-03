import dynamicGameObject

SPEED = -6

class SpaceShip(dynamicGameObject.DynamicGameObject):
    def __init__(self, topright):
        dynamicGameObject.DynamicGameObject.__init__(self, SPEED, topright=topright)
        self.points = 5

    def update(self):
        self.rect.move_ip((self.speed, 0))
        if self.rect.right <= self.screenRect.left:
            self.kill()