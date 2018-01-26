# /F50/ Die Aliens muss nach unten schießen. Wird dabei die Kanone getroffen, verliert der Spieler eines seiner Leben.
#  -*- encodig: utf-8 -*-
___author___ = 'Nowodworski, Kossjak'

import dynamicGameObject

SPEED = 8


class AlienBullet(dynamicGameObject.DynamicGameObject):

    points = 2

    def __init__(self, position):
        dynamicGameObject.DynamicGameObject.__init__(self, SPEED, midbottom=position)

    def update(self):
        self.rect.move_ip((0, self.speed))
        if self.rect.bottom >= self.screenRect.bottom:
            self.kill()