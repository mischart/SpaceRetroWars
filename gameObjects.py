# -*- encodig: utf-8 -*-
___author___ = 'Nowodworski, Kossjak'

import pygame, util


# Klasse zum Repraesentieren von Spielobjekten
class GameObject(pygame.sprite.Sprite):
    image = None

    def __init__(self, midbottom=None, topright=None, center=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        if midbottom:
            self.rect = self.image.get_rect(midbottom=midbottom)
        elif topright:
            self.rect = self.image.get_rect(topright=topright)
        elif center:
            self.rect = self.image.get_rect(center=center)
        else:
            self.rect = self.image.get_rect()
        self.screenRect = util.get_screen_rect()


# Klasse zum Repraesentieren der Spielobjekte
# die sich bewegen koennen
class DynamicGameObject(GameObject):
    def __init__(self, speed, midbottom=None, topright=None, center=None):
        GameObject.__init__(self, midbottom, topright, center)
        self.speed = speed

    def update(self):
        raise NotImplementedError("Subclasses should have implemented this")


# /F20/ Das Spiel muss dem Spieler ermöglichen, am unteren Rand
# des Spielfeldes eine Kanone horizontal nach rechts und nach links zu steuern.

CANON_SPEED = 10


# Klasse zum Repraesentieren der Kanone,
# die von dem Spieler gesteuert wird
class Canon(DynamicGameObject):
    def __init__(self, position):
        DynamicGameObject.__init__(self, CANON_SPEED, midbottom=position)
        self.mode = 'stop'
        self.lifes = 3

    def update(self):
        newPos = None
        if self.mode == 'moveRight':
            newPos = self.rect.move((self.speed, 0))
        if self.mode == 'moveLeft':
            newPos = self.rect.move((-self.speed, 0))

        if newPos:
            if newPos.left >= self.screenRect.left and \
                            newPos.right <= self.screenRect.right:
                self.rect = newPos

    def getPosition(self):
        return self.rect.midtop

    def moveRight(self):
        self.mode = 'moveRight'

    def moveLeft(self):
        self.mode = 'moveLeft'

    def stop(self):
        self.mode = 'stop'


# /F30/ Während des Spiels muss sich mehrere Reihen von Objekten (Aliens), die parallel zueinander angeordnet sind, horizontal von links nach rechts und zurück bewegen. Nach dem Erreichen eines Bereichs des linken bzw. des rechten Spielfeldrandes müssen die Reihen von Aliens um denselben Bereich nach unten verschoben werden.

# Klasse zum Repraesentieren von Aliens
class Alien(DynamicGameObject):
    goDown = False
    capture = False
    alienMatrix = None  # Matrix mit Aliens

    def __init__(self, speed, position=None):
        DynamicGameObject.__init__(self, speed, midbottom=position)
        self.points = 1

    def update(self, lower=False):
        if not lower:
            self.rect.move_ip(self.speed, 0)
            if self.rect.left < self.screenRect.left or \
                            self.rect.right > self.screenRect.right:
                Alien.goDown = True
        else:
            self.speed = -self.speed  # Aenderung der Bewegungsrichtung
            self.rect.move_ip(self.speed, 30)

        if self.rect.bottom >= self.screenRect.bottom:
            Alien.capture = True
            self.kill()

    def getPosition(self):
        return self.rect.midbottom

    def kill(self):
        for i in range(len(Alien.alienMatrix)):
            for j in range(len(Alien.alienMatrix[i])):
                if self is Alien.alienMatrix[i][j]:
                    # Matrix-Elemente, die eliminierte Aliens darstellen verschieben
                    Alien.__move_matrixitem_to_initial_row(i, j)
                    break
        pygame.sprite.Sprite.kill(self)

    # Methode zum Verschieben von Matrix-Elementen
    @classmethod
    def __move_matrixitem_to_initial_row(cls, item_row, item_column):
        if item_row > 0:
            item_in_lower_row = Alien.alienMatrix[item_row - 1][item_column]
            if item_in_lower_row:
                Alien.alienMatrix[item_row][item_column] = item_in_lower_row
                Alien.alienMatrix[item_row - 1][item_column] = None
                Alien.__move_matrixitem_to_initial_row(item_row - 1, item_column)
            else:
                Alien.alienMatrix[item_row][item_column] = None
        else:
            Alien.alienMatrix[item_row][item_column] = None


BULLET_SPEED = -5


# Klasse zum Repraesentieren der Geschosse des Spielers
class Bullet(DynamicGameObject):
    def __init__(self, position):
        DynamicGameObject.__init__(self, BULLET_SPEED, midbottom=position)

    def update(self):
        self.rect.move_ip((0, self.speed))
        if self.rect.top <= self.screenRect.top:
            self.kill()


BOMB_SPEED = -1


# Klasse zum Repraesentieren der Bomben des Spielers
class Bomb(DynamicGameObject):
    price = 2

    def __init__(self, position):
        DynamicGameObject.__init__(self, BOMB_SPEED, midbottom=position)

    def update(self):
        self.rect.move_ip((0, self.speed))
        if self.rect.top <= self.screenRect.top:
            self.kill()


DECASTLING_SPEED = -50


# Klasse zum Repraesentieren von Decastling
class Decastling(DynamicGameObject):
    price = 3

    def __init__(self, midbottom):
        DynamicGameObject.__init__(self, DECASTLING_SPEED, midbottom=midbottom)

    def update(self):
        self.rect.move_ip((0, self.speed))
        if self.rect.top <= self.screenRect.top:
            self.kill()


# /F50/ Die Aliens muss nach unten schießen. Wird dabei die Kanone getroffen, verliert der Spieler eines seiner Leben.
#  -*- encodig: utf-8 -*-

ALIEN_BULLET_SPEED = 8


# Klasse zum Repraesentieren der Geschosse der Aliens
class AlienBullet(DynamicGameObject):
    points = 2

    def __init__(self, position):
        DynamicGameObject.__init__(self, ALIEN_BULLET_SPEED, midbottom=position)

    def update(self):
        self.rect.move_ip((0, self.speed))
        if self.rect.bottom >= self.screenRect.bottom:
            self.kill()


ASTEROID_SPEED = 8


# Klasse zum Repraesentieren der Asteroiden
class Asteroid(DynamicGameObject):
    price = 4

    def __init__(self, position):
        DynamicGameObject.__init__(self, ASTEROID_SPEED, topright=position)

    def update(self):
        self.rect.move_ip((0, self.speed))
        if self.rect.bottom >= self.screenRect.bottom:
            self.kill()


BLACK_HOLE_SPEED = 9


# Klasse zum Repraesentieren der schwarzen Loecher
class BlackHole(DynamicGameObject):
    def __init__(self, position):
        DynamicGameObject.__init__(self, BLACK_HOLE_SPEED, topright=position)

    def update(self):
        self.rect.move_ip((0, self.speed))
        if self.rect.bottom >= self.screenRect.bottom:
            self.kill()


# /F70/ Ab und zu muss im oberen Bereich des Spielfeldes ein Raumschiff erscheinen, das sich horizontal von einem Spielfeldrand bis zum anderen bewegt. Wird er durch die Kanone getroffen, bekommt der Spieler eine bestimmte Anzahl von Punkten.
SPACE_SHIP_SPEED = -6


# Klasse zum Repraesentieren von SpaceShips
class SpaceShip(DynamicGameObject):
    def __init__(self, topright):
        DynamicGameObject.__init__(self, SPACE_SHIP_SPEED, topright=topright)
        self.points = 5

    def update(self):
        self.rect.move_ip((self.speed, 0))
        if self.rect.right <= self.screenRect.left:
            self.kill()


# /F60/ Über der Kanone müssen sich Blöcke befinden, hinter denen sich die Kanone verstecken kann.

# Klasse zum Repraesentieren der Bloecke
class Wall(pygame.sprite.Sprite):
    image = None

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Wall.image
        self.rect = self.image.get_rect(x=position[0], y=position[1])


START_LIFES = 12


# Klasse zum Repraesentieren des Feuers nach der Explosion
class Fire(GameObject):
    images = None
    animation_cycle = 3

    def __init__(self, center):
        GameObject.__init__(self, center=center)
        self.lifes = START_LIFES

    def update(self):
        self.lifes = self.lifes - 1
        self.image = self.images[self.lifes // self.animation_cycle % 2]
        if self.lifes <= 0: self.kill()
