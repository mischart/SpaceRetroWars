import dynamicGameObject


class SpaceShip(dynamicGameObject.DynamicGameObject):
    def __init__(self, speed, xy):
        dynamicGameObject.DynamicGameObject.__init__(self, speed, xy)

    def update(self):
        self.rect.move_ip((self.speed, 0))
        if self.rect.left <= self.screenRect.left:
            self.kill()
