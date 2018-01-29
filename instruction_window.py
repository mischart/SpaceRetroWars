import util, pygame
from pygame.locals import *
from button import Button
from state import State


# Klasse zur Darstellung der Spielanleitung
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

        font = pygame.font.Font(None, 40)
        x = 50
        distance_x = 260
        y = 100
        distance_y = 40

        text1 = "Pfeil-links-Taste"
        text2 = "Bewegung nach links"
        self.blit_text_line(screen, font, x, y, distance_x, text1, text2)

        y += distance_y
        text1 = "Pfeil-rechts-Taste"
        text2 = "Bewegung nach rechts"
        self.blit_text_line(screen, font, x, y, distance_x, text1, text2)

        y += distance_y
        text1 = "Pfeil-oben-Taste"
        text2 = "Schuss"
        self.blit_text_line(screen, font, x, y, distance_x, text1, text2)

        y += distance_y
        text2 = "Im Spielfeld kann sich nur 1"
        self.blit_text_line(screen, font, x, y, distance_x, text2=text2)

        y += distance_y
        text2 = "Geschoss befinden"
        self.blit_text_line(screen, font, x, y, distance_x, text2=text2)

        y += distance_y
        text1 = "Taste A"
        text2 = "Asteroidenregen (Punktabzug)"
        self.blit_text_line(screen, font, x, y, distance_x, text1, text2)

        y += distance_y
        text1 = "Taste S"
        text2 = "Bombe (Punktabzug)"
        self.blit_text_line(screen, font, x, y, distance_x, text1, text2)

        y += distance_y
        text1 = "Taste D"
        text2 = "Decastling (Punktabzug)"
        self.blit_text_line(screen, font, x, y, distance_x, text1, text2)

        y += distance_y
        text1 = "3 Levels"
        self.blit_text_line(screen, font, x, y, distance_x, text1)

        y += distance_y
        text1 = "nur nach Spielgewinn wird das Ergebnis gespeichert"
        self.blit_text_line(screen, font, x, y, distance_x, text1)

        y += distance_y
        text1 = "Endergebnis = Leben X erreichte Punkte"
        self.blit_text_line(screen, font, x, y, distance_x, text1)

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

    @staticmethod
    def blit_text_line(screen, font, x, y, distance_x, text1=None, text2=None):
        if text1:
            text1 = font.render(text1, True, Color('Red'))
            screen.blit(text1, (x, y))
        if text2:
            text2 = font.render(text2, True, Color('White'))
            screen.blit(text2, (x + distance_x, y))
