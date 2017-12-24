import pygame, util


class Bullet(pygame.sprite.Sprite):
    speed = -5
    image = None
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Bullet.image
        self.rect = self.image.get_rect(midbottom=position)
        self.screenRect = util.get_screen_rect()

    def update(self):
        self.rect.move_ip((0, Bullet.speed))
        if self.rect.top <= self.screenRect.top:
            self.kill()