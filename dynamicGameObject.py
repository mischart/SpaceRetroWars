import pygame, gameObject, util


class DynamicGameObject(gameObject.GameObject):
    def __init__(self, speed, midbottom=None, topright=None):
        gameObject.GameObject.__init__(self, midbottom, topright)
        self.speed = speed

    def update(self):
        raise NotImplementedError("Subclasses should have implemented this")