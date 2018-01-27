import pygame, util


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