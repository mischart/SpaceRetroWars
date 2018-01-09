import pygame, util


class Bombe(pygame.sprite.Sprite):
    speed = -1
    image = None

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Bombe.image
        self.rect = self.image.get_rect(midbottom=position)
        self.screenRect = util.get_screen_rect()

    def update(self):
        self.rect.move_ip((0, Bombe.speed))
        if self.rect.top <= self.screenRect.top:
            self.kill()