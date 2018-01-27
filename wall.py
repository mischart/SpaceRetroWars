# /F60/ Über der Kanone müssen sich Blöcke befinden, hinter denen sich die Kanone verstecken kann. Die Blöcke können durch ein Geschoss sowohl von den Aliens als auch von der Kanone getroffen werden, sodass sie letztendlich zerstört werden.
#  -*- encodig: utf-8 -*-
___author___ = 'Nowodworski, Kossjak'

import pygame


class Wall(pygame.sprite.Sprite):
    image = None

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Wall.image
        self.rect = self.image.get_rect(x=position[0], y=position[1])