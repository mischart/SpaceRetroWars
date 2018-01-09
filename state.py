# /F10/ Vor dem Spielbeginn muss dem Spieler gewährleistet werden, eine von mindestens zwei Spielumgebungen auszuwählen.
class State(object):
    settings_dict = {
        'player_name': None,
        'game_background': None,
        'schwierigkeitsgrad': None
    }

    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
        self.active_text_input = False