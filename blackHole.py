# -*- encodig: utf-8 -*-
___author___ = 'Nowodworski, Kossjak'

import pygame, util


class BlackHole(pygame.sprite.Sprite):
    speed = 9
    image = None

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = BlackHole.image
        self.rect = self.image.get_rect(midbottom=position)
        self.screenRect = util.get_screen_rect()

    def update(self):
        self.rect.move_ip((0, BlackHole.speed))
        if self.rect.bottom >= self.screenRect.bottom:
            self.kill()