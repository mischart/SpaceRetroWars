# /F30/ Während des Spiels muss sich mehrere Reihen von Objekten (Aliens), die parallel zueinander angeordnet sind, horizontal von links nach rechts und zurück bewegen. Nach dem Erreichen eines Bereichs des linken bzw. des rechten Spielfeldrandes müssen die Reihen von Aliens um denselben Bereich nach unten verschoben werden.
# -*- encodig: utf-8 -*-
___author___ = 'Nowodworski, Kossjak'

import pygame, util


class Alien(pygame.sprite.Sprite):
    image = None
    goDown = False
    capture = False
    alienMatrix = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Alien.image
        self.rect = self.image.get_rect()
        self.speed = 5
        self.screenRect = util.get_screen_rect()
        self.points = 1

    def update(self, lower=False):
        if not lower:
            self.rect.move_ip(self.speed, 0)
            if self.rect.left < self.screenRect.left or \
                            self.rect.right > self.screenRect.right:
                Alien.goDown = True
        else:
            self.speed = -self.speed
            self.rect.move_ip(self.speed, 30)

        if self.rect.bottom >= self.screenRect.bottom:
            Alien.capture = True
            self.kill()

    # die Klasse Sprite hat bereits eine Methode remove zum Entfernen des Sprites von  der Gruppe
    # Wir sollen die Methode nicht überschreiben
    # def remove(self):
    #     print ("remove")
    #     self.kill()

    def getPosition(self):
        return self.rect.midbottom

    def kill(self):
        for i in range(len(Alien.alienMatrix)):
            for j in range(len(Alien.alienMatrix[i])):
                if self is Alien.alienMatrix[i][j]:
                    Alien.move_matrixitem_to_initial_row(i, j)
                    break
        pygame.sprite.Sprite.kill(self)

    @classmethod
    def move_matrixitem_to_initial_row(cls, item_row, item_column):
        if item_row > 0:
            item_in_lower_row = Alien.alienMatrix[item_row - 1][item_column]
            if item_in_lower_row:
                Alien.alienMatrix[item_row][item_column] = item_in_lower_row
                Alien.alienMatrix[item_row - 1][item_column] = None
                Alien.move_matrixitem_to_initial_row(item_row - 1, item_column)
            else:
                Alien.alienMatrix[item_row][item_column] = None
        else:
            Alien.alienMatrix[item_row][item_column] = None