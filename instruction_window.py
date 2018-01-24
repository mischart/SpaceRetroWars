import util, pygame
from pygame.locals import *
from button import Button
from state import State


class InstructionWindow(State):
    def __init__(self, images, fonts):
        State.__init__(self)
        self.next = 'start_menu'
        self.background = images[0]
        self.fonts = fonts
        self.buttons = pygame.sprite.Group()
        Button.groups = self.buttons
        screen_size = pygame.display.get_surface().get_size()
        self.back_button = Button((images[1], images[2]),
                                  (screen_size[0] - 140, screen_size[1] - self.y_for_bottom_buttons))

    def cleanup(self):
        self.set_buttons_to_unfocused(self.buttons)

    def startup(self):
        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))
        instruction_text = self.fonts[0].render('SPIELANLEITUNG', True, Color('White'))
        screen.blit(instruction_text, (50, 10))
        pygame.draw.rect(screen, pygame.Color('Black'), self.bottom_menu_box)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.rect.collidepoint(pygame.mouse.get_pos()):
                self.done = True
        elif event.type == pygame.MOUSEMOTION:
            self.set_buttons_to_unfocused(self.buttons)
            self.set_buttons_to_focused(self.buttons)

    def update(self, screen):
        pygame.draw.rect(screen, pygame.Color('Black'), self.bottom_menu_box)
        self.buttons.update()
        self.buttons.draw(screen)
