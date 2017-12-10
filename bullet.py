import pygame, util

class Bullet(pygame.sprite.Sprite):

    def __init__(self, canon):
        pygame.sprite.Sprite.__init__(self)
        self.image = util.load_image('bullet.png')
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        #TO DO bullet wird in de Mitte des screens gesetzt, soll aber da wo die Kanone ist erscheinen!
        screen = pygame.display.get_surface()
        self.screenRect = screen.get_rect()
        self.rect.midbottom = self.screenRect.midbottom

    def update(self, spriteGroup, bullet):
        newPos = None
        if self.mode == 'moveUp':
            newPos = self.rect.move((0, -5))

        if newPos:
            if newPos.top >= self.screenRect.top:
                self.rect = newPos
            else:
                spriteGroup.remove(bullet)

    def moveUp(self, spriteGroup, bullet):
        self.mode = 'moveUp'
