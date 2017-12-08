import pygame, util


class Canon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = util.load_image('canon.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.mode = 'stop'
        self.speed = 10

        screen = pygame.display.get_surface()
        self.screenRect = screen.get_rect()
        self.rect.midbottom = self.screenRect.midbottom
        # self.newPos = self.rect.copy()

    def update(self):
        newPos = None
        if self.mode == 'moveRight':
            newPos = self.rect.move((self.speed, 0))
        if self.mode == 'moveLeft':
            newPos = self.rect.move((-self.speed, 0))

        if newPos:
            newLeft = newPos.left
            newRight = newPos.right
            areaLeft = self.screenRect.left
            areaRight = self.screenRect.right

            if newPos.left >= self.screenRect.left and \
                            newPos.right <= self.screenRect.right:
                self.rect = newPos

    def moveRight(self):
        self.mode = 'moveRight'

    def moveLeft(self):
        self.mode = 'moveLeft'

    def stop(self):
        self.mode = 'stop'
