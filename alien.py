# /F30/ Während des Spiels muss sich mehrere Reihen von Objekten (Aliens), die parallel zueinander angeordnet sind, horizontal von links nach rechts und zurück bewegen. Nach dem Erreichen eines Bereichs des linken bzw. des rechten Spielfeldrandes müssen die Reihen von Aliens um denselben Bereich nach unten verschoben werden.
# -*- encodig: utf-8 -*-
___author___ = 'Nowodworski, Kossjak'

import pygame, dynamicGameObject


# Klasse zum Repraesentieren von Aliens
class Alien(dynamicGameObject.DynamicGameObject):
    goDown = False
    capture = False
    alienMatrix = None  # Matrix mit Aliens

    def __init__(self, speed, position=None):
        dynamicGameObject.DynamicGameObject.__init__(self, speed, midbottom=position)
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
