import pygame, util


class Railgun(pygame.sprite.Sprite):
    speed = -50
    image = None
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Railgun.image
        self.rect = self.image.get_rect(midbottom=position)
        self.screenRect = util.get_screen_rect()

    def update(self):
        self.rect.move_ip((0, Railgun.speed))
        if self.rect.top <= self.screenRect.top:
            self.kill()