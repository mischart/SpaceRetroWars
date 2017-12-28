import dynamicGameObject


class SpaceShip(dynamicGameObject.DynamicGameObject):
    def __init__(self, speed, topright):
        dynamicGameObject.DynamicGameObject.__init__(self, speed, topright=topright)
        self.points = 30

    def update(self):
        self.rect.move_ip((self.speed, 0))
        if self.rect.right <= self.screenRect.left:
            self.kill()