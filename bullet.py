import dynamicGameObject

SPEED = -5


class Bullet(dynamicGameObject.DynamicGameObject):
    def __init__(self, position):
        dynamicGameObject.DynamicGameObject.__init__(self, SPEED, midbottom=position)

    def update(self):
        self.rect.move_ip((0, self.speed))
        if self.rect.top <= self.screenRect.top:
            self.kill()