# -*- encodig: utf-8 -*-
___author___ = 'Nowodworski, Kossjak'

import dynamicGameObject

SPEED = 9


class BlackHole(dynamicGameObject.DynamicGameObject):
    def __init__(self, midbottom):
        dynamicGameObject.DynamicGameObject.__init__(self, SPEED, midbottom=midbottom)

    def update(self):
        self.rect.move_ip((0, self.speed))
        if self.rect.bottom >= self.screenRect.bottom:
            self.kill()