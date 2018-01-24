# /F10/ Vor dem Spielbeginn muss dem Spieler gewährleistet werden, eine von mindestens zwei Spielumgebungen auszuwählen.

import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, images, topleft):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect(topleft=topleft)
        self.focused = False
        self.clicked = False
        self.dirty = False

    def update(self):
        if self.dirty:
            if self.clicked or self.focused:
                self.image = self.images[1]
            else:
                self.image = self.images[0]
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
            self.dirty = False

    def set_clicked(self, clicked):
        self.clicked = clicked
        self.dirty = True

    def set_focused(self, focused):
        self.focused = focused
        self.dirty = True