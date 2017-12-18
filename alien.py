# -*- encodig: utf-8 -*-
___author___ = 'Nowodworski, Kossjak'

import pygame, util


class Alien(pygame.sprite.Sprite):
    image = None
    goDown = False
    capture = False

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Alien.image
        self.rect = self.image.get_rect()
        self.speed = 15
        self.screenRect = util.get_screen_rect()

    def update(self, lower=False):
        if not lower:
            self.rect.move_ip(self.speed, 0)
            if self.rect.left < self.screenRect.left or \
                            self.rect.right > self.screenRect.right:
                Alien.goDown = True
        else:
            self.speed = -self.speed
            self.rect.move_ip(self.speed, 30)

        if self.rect.bottom >= self.screenRect.bottom - 50:
            Alien.capture = True

    def spin(self):
        self.dizzy = 1
        self.original = self.image
        "spin the image"
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def remove(self):
        print ("remove")
        self.kill()

    def getPosition(self):
        return self.rect.midbottom