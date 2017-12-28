import pygame, util


class GameObject(pygame.sprite.Sprite):
    image = None

    def __init__(self, midbottom, topright):
        pygame.sprite.Sprite.__init__(self, self.groups)
        if midbottom:
            self.rect = self.image.get_rect(midbottom=midbottom)
        if topright:
            self.rect = self.image.get_rect(topright=topright)
        self.screenRect = util.get_screen_rect()
