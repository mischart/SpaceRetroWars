class State(object):
    settings_dict = {
        'player_name': None,
        'game_background': None
    }

    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
        self.active_text_input = False