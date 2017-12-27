import pygame, gameObject, util


class DynamicGameObject(gameObject.GameObject):
    def __init__(self, speed, midbottom=None, xy=None):
        pygame.sprite.Sprite.__init__(self, self.groups)
        gameObject.GameObject.__init__(self, midbottom, xy)
        self.speed = speed

    def update(self):
        raise NotImplementedError("Subclasses should have implemented this")
