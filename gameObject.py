import pygame, util


class GameObject(pygame.sprite.Sprite):
    image = None

    def __init__(self, midbottom, xy):
        pygame.sprite.Sprite.__init__(self, self.groups)
        if midbottom:
            self.rect = self.image.get_rect(midbottom=midbottom)
        if xy:
            self.rect.x = xy[0]
            self.rect.y = xy[1]
        self.screenRect = util.get_screen_rect()
