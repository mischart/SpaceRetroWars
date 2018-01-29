import util, pygame
from pygame.locals import *
from button import Button
from state import State


# Klasse zur Darstellung der besten Ergebnisse
class ScoreWindow(State):
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
        # lesender Zugriff auf die DB
        self.high_score = util.get_highscore_results()

        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))
        high_score_text = self.fonts[0].render('HIGHSCORE', True, Color('White'))
        screen.blit(high_score_text, (175, 10))
        self.__show_high_score()
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
        pygame.display.flip()

    # Highscore Anzeige
    def __show_high_score(self):
        default_font = pygame.font.Font(None, 40)

        # Highscore Überschrift
        point_title = default_font.render('Punkte', True, Color('Red'))
        width_of_point_title = point_title.get_size()[0]
        date_title = default_font.render('Erreicht am', True, Color('Red'))
        width_of_date_title = date_title.get_size()[0]
        name_title = default_font.render('von', True, Color('Red'))

        start_x = 100
        distance_between_columns = 80
        start_y = 100
        screen = pygame.display.get_surface()

        # erste Spalte der Anzeige
        x_y_of_points_row = (start_x, start_y)
        screen.blit(point_title, x_y_of_points_row)

        # zweite Spalte der Anzeige
        x = start_x + width_of_point_title + distance_between_columns
        x_y_of_date_row = (x, start_y)
        screen.blit(date_title, x_y_of_date_row)

        # dritte Spalte der Anzeige
        x += distance_between_columns + width_of_date_title
        x_y_of_name_row = (x, start_y)
        screen.blit(name_title, x_y_of_name_row)

        # Highscore wird aus den Zeilen der Variablen high_score herausgelesen und auf dem screen angezeigt
        counter = 0
        delta_y = 20
        for row in self.high_score:
            counter += 1
            if counter < 11:
                delta_y += 25
                point_text = default_font.render(row[0], True, Color('White'))
                date_text = default_font.render(row[1], True, Color('White'))
                name_text = default_font.render(row[2], True, Color('White'))

                screen.blit(point_text, (x_y_of_points_row[0], x_y_of_points_row[1] + delta_y))
                screen.blit(date_text, (x_y_of_date_row[0], x_y_of_date_row[1] + delta_y))
                screen.blit(name_text, (x_y_of_name_row[0], x_y_of_name_row[1] + delta_y))

            else:
                break
