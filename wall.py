# -*- encodig: utf-8 -*-
___author___ = 'Nowodworski, Kossjak'

import pygame, util


class Wall(pygame.sprite.Sprite):
    image = None

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Wall.image
        self.rect = self.image.get_rect(x=position[0], y=position[1])
