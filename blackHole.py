# -*- encodig: utf-8 -*-
___author___ = 'Nowodworski, Kossjak'

import dynamicGameObject

SPEED = 9


class BlackHole(dynamicGameObject.DynamicGameObject):
    def __init__(self, position):
        dynamicGameObject.DynamicGameObject.__init__(self, SPEED, topright=position)

    def update(self):
        self.rect.move_ip((0, self.speed))
        if self.rect.bottom >= self.screenRect.bottom:
            self.kill()