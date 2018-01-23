# /F10/ Vor dem Spielbeginn muss dem Spieler gewährleistet werden, eine von mindestens zwei Spielumgebungen auszuwählen.
# Import and Initialization
import pygame, util, pygame_textinput
from pygame.locals import *
from button import Button
from state import State


class StartMenu(State):
    def __init__(self, images, fonts):
        State.__init__(self)
        self.next = 'game'
        self.background = images[0]
        self.fonts = fonts
        self.farbeaendern = 0
        self.start_window_text_1 = self.fonts[0].render('SPACE', True, Color('White'))
        self.start_window_text_2 = self.fonts[0].render('WARS', True, Color('White'))
        self.text_input = pygame_textinput.TextInput()
        self.high_score = None
        self.text_input_box = pygame.Rect(50, 140, 300, 40)
        default_font = pygame.font.Font(None, 35)
        self.name_text = default_font.render('Name:', True, Color('Cyan'))

        self.bg_text = default_font.render('Spielumgebung:', True, Color('Cyan'))
        self.bg_box = pygame.Rect(self.text_input_box.x, self.text_input_box.y + 100, 300, 130)
        self.buttons = pygame.sprite.Group()
        Button.groups = self.buttons
        self.screen_button_1 = Button((images[1], images[2]), (self.bg_box.x + 20, self.bg_box.y + 20))
        self.screen_button_1.set_clicked(True)
        self.screen_button_2 = Button((images[3], images[4]), (self.bg_box.x + 150, self.bg_box.y + 20))

        #self.play_button = Button((images[5], images[6]), (self.bg_box.x, self.bg_box.y + 270))

        # images[5] entspricht der Normalansicht und images[6] wenn mit der Maus darauf gezeigt wird
        self.play_box = pygame.Rect(self.bg_box.x, self.bg_box.y + 190, 300, 130)
        self.play_text = default_font.render('Spiel starten:', True, Color('Cyan'))
        self.difficulty_5x5_button = Button((images[7], images[8]), (self.play_box.x + 20, self.play_box.y + 20))
        self.difficulty_6x6_button = Button((images[9], images[10]), (self.play_box.x + 115, self.play_box.y + 20))
        self.difficulty_7x7_button = Button((images[11], images[12]), (self.play_box.x + 210, self.play_box.y + 20))

    def cleanup(self):
        print('cleaning up Menu state stuff')
        pygame.mixer.music.stop()

        # player_name = State.settings_dict['player_name']
        player_name = self.text_input.get_text()
        if not player_name or player_name == "":
            State.settings_dict['player_name'] = "anonymous"
        else:
            State.settings_dict['player_name'] = player_name
        self.text_input.clean_up()

        if self.screen_button_1.clicked:
            #print("screen_button_1.clicked")
            State.settings_dict['game_background'] = 1
        else:
            State.settings_dict['game_background'] = 2
        self.set_button_to_unfocused()
        self.screen_button_1.set_clicked(True)
        self.screen_button_2.set_clicked(False)

    def startup(self):
        print('starting Menu state stuff')
        # TODO checken, ob man die mp3-Datei schon früher (zusammen mit den anderen Sounds) laden kann
        pygame.mixer.music.load('data/Menue.mp3')
        pygame.mixer.music.play(-1)
        self.high_score = util.get_highscore_results()

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            print('Menu State keydown')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # TODO or Enter and close window when click on X
            # TODO: das Play-Image separat laden und dann mit playimage.get_rect().collidepoint(pygame.mouse.get_pos())
            # prüfen, ob sich der der Mause-Pointer innerhalb des Play-Images befindet
            if self.text_input_box.collidepoint(pygame.mouse.get_pos()):
                self.active_text_input = True
            else:
                self.active_text_input = False
            if self.screen_button_1.rect.collidepoint(pygame.mouse.get_pos()):
                self.screen_button_1.set_clicked(True)
                self.screen_button_2.set_clicked(False)
            if self.screen_button_2.rect.collidepoint(pygame.mouse.get_pos()):
                self.screen_button_2.set_clicked(True)
                self.screen_button_1.set_clicked(False)

            #if self.play_button.rect.collidepoint(pygame.mouse.get_pos()):
                #self.done = True
            if self.difficulty_5x5_button.rect.collidepoint(pygame.mouse.get_pos()):
                print("start_menu.py difficulty_5x5_button clicked")
                State.settings_dict['degree_of_difficulty'] = 5
                self.done = True
            if self.difficulty_6x6_button.rect.collidepoint(pygame.mouse.get_pos()):
                print("start_menu.py difficulty_6x6_button clicked")
                State.settings_dict['degree_of_difficulty'] = 6
                self.done = True
            if self.difficulty_7x7_button.rect.collidepoint(pygame.mouse.get_pos()):
                print("start_menu.py difficulty_7x7_button clicked")
                State.settings_dict['degree_of_difficulty'] = 7
                self.done = True

        elif event.type == pygame.MOUSEMOTION:
            self.set_button_to_unfocused()
            for button in self.buttons:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.set_focused(True)

    def get_events_to_text_input(self, events):
        self.text_input.update(events)

    def update(self, screen):
        # Start Screen Überschrift
        screen.blit(self.background, (0, 0))
        screen.blit(self.start_window_text_1, [10, 10])
        screen.blit(self.start_window_text_2, [screen.get_width() - 250, 10])
        self.show_high_score(screen)
        self.farbeaendern += 1
        if self.farbeaendern < 10:
            retro_color = Color('Yellow')
        elif self.farbeaendern < 20:
            retro_color = Color('Red')
        elif self.farbeaendern < 30:
            retro_color = Color('Green')
        elif self.farbeaendern < 40:
            retro_color = Color('Blue')
        elif self.farbeaendern < 50:
            retro_color = Color('Cyan')
        elif self.farbeaendern < 60:
            retro_color = Color('Magenta')
        else:
            retro_color = Color('Yellow')
            self.farbeaendern = 0

        retro_text = self.fonts[1].render('RETRO', True, retro_color)
        screen.blit(retro_text, [screen.get_width() - 510, 5])
        # screen.blit(retro_text, [screen.get_width() / 3, screen.get_height() - 75])

        screen.blit(self.name_text, (self.text_input_box.x, self.text_input_box.y - 30))
        pygame.draw.rect(screen, pygame.Color('White'), self.text_input_box)
        screen.blit(self.text_input.get_surface(), (self.text_input_box.x + 4, self.text_input_box.y + 4))
        pygame.draw.rect(screen, pygame.Color('White'), self.bg_box)
        screen.blit(self.bg_text, (self.bg_box.x, self.bg_box.y - 30))

        pygame.draw.rect(screen, pygame.Color('White'), self.play_box)
        screen.blit(self.play_text, (self.play_box.x, self.play_box.y - 30))

        self.buttons.update()
        self.buttons.draw(screen)
        # pygame.display.flip()

    def set_button_to_unfocused(self):
        for button in self.buttons:
            button.set_focused(False)

    def draw(self, screen):
        pass

    # /F90/ Es muss möglich sein, die Liste der besten Spielergebnisse aufzurufen (lokal).
    def show_high_score(self, screen):
        # Highscore Anzeige
        zeilen = 100

        # Highscore Überschrift
        start_window_highscore = self.fonts[3].render('Punkte   Erreicht am   von', True, Color('White'))
        screen.blit(start_window_highscore, [screen.get_width() / 7, zeilen])

        # Highscore wird aus den Zeilen der Tabelle sw aus der Datenbank Highscore2 herausgelesen und auf dem screen angezeigt
        top10 = 0
        for row in self.high_score:
            top10 += 1
            if top10 < 11:
                highscoreText = '    '
                for columns in range(0, 3):
                    highscoreText = highscoreText + row[columns] + '        '
                # print(highscoreText)
                start_window_highscore = self.fonts[3].render(highscoreText, True, Color('White'))
                screen.blit(start_window_highscore, [screen.get_width() / 7, 25 * columns + zeilen + 10])
                zeilen += 25