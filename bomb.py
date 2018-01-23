import dynamicGameObject

SPEED = -1


class Bomb(dynamicGameObject.DynamicGameObject):
    price = 2

    def __init__(self, position):
        dynamicGameObject.DynamicGameObject.__init__(self, SPEED, midbottom=position)

    def update(self):
        self.rect.move_ip((0, self.speed))
        if self.rect.top <= self.screenRect.top:
            self.kill()
