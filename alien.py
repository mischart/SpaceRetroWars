import pygame, util


class Alien(pygame.sprite.Sprite):
    image = None
    goDown = False
    capture = False

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = Alien.image
        self.rect = self.image.get_rect()
        self.speed = 5
        self.screenRect = util.get_screen_rect()

    def update(self, lower=False):
        if not lower:
            self.rect.move_ip(self.speed, 0)
            if self.rect.left < self.screenRect.left or \
                            self.rect.right > self.screenRect.right:
                Alien.goDown = True
        else:
            self.speed = -self.speed
            self.rect.move_ip(self.speed, 30)

        if self.rect.bottom >= self.screenRect.bottom - 50:
            Alien.capture = True
