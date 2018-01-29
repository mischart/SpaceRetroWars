import dynamicGameObject

SPEED = -50


# Klasse zum Repraesentieren von Decastling
class Decastling(dynamicGameObject.DynamicGameObject):
    price = 3

    def __init__(self, midbottom):
        dynamicGameObject.DynamicGameObject.__init__(self, SPEED, midbottom=midbottom)

    def update(self):
        self.rect.move_ip((0, self.speed))
        if self.rect.top <= self.screenRect.top:
            self.kill()
