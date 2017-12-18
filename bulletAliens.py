import pygame


class BulletAliens(pygame.sprite.Sprite):
    speed = 9
    image = None
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = BulletAliens.image
        self.rect = self.image.get_rect(midbottom=position)
        screen = pygame.display.get_surface()
        self.screenRect = screen.get_rect()

    def update(self):
        self.rect.move_ip((0, BulletAliens.speed))
        if self.rect.bottom >= self.screenRect.bottom:
            self.kill()
