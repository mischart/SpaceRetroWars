import pygame


# Klasse State zur Implementierung eines Zustandsautomaten (State Pattern)
# Auf der Basis der Quelle: http://python-gaming.com/pygame/docs/tuts/state_machine.html
class State(object):
    game_settings = {
        'player_name': None,
        'game_background': None,
        'degree_of_difficulty': None
    }

    bottom_menu_box = pygame.Rect(0, 600 - 60, 800, 60)
    y_for_bottom_buttons = 52

    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
        self.active_text_input = False

    @staticmethod
    def set_buttons_to_unfocused(buttons):
        for button in buttons:
            button.set_focused(False)

    @staticmethod
    def set_buttons_to_focused(buttons):
        for button in buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                button.set_focused(True)
