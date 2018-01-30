import pygame, util
from game_objects import *
from game import Game
from start_menu import StartMenu
from score_window import ScoreWindow
from instruction_window import InstructionWindow


# Klasse Control zur Implementierung eines Zustandsautomaten (State Pattern)
# Auf der Basis der Quelle: http://python-gaming.com/pygame/docs/tuts/state_machine.html
class Control:
    def __init__(self, screen_size):
        self.done = False
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('Space Retro Wars')
        pygame.display.set_icon(util.load_image('LogoIcon256.jpg'))
        self.clock = pygame.time.Clock()

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup()

    # Zustand (Spiel-Fenster) wechseln
    def __flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous

    # Zustand und Anzeige aktualisieren
    def __update(self):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.__flip_state()
        self.state.update(self.screen)

    # events ueberpruefen
    def __event_loop(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)
        if self.state.active_text_input:
            self.state.get_events_to_text_input(events)

    # Spiel-Schleife
    def main_game_loop(self):
        while not self.done:
            self.clock.tick(30)
            self.__event_loop()
            self.__update()


# Entities laden
def init_game():
    pygame.init()
    # Fonts laden
    start_menu_fonts = []
    start_menu_fonts.append(pygame.font.SysFont('SPACEBOY', 56, False, False))
    start_menu_fonts.append(pygame.font.SysFont('Space Cruiser', 56, False, True))
    start_menu_fonts.append(pygame.font.SysFont('SPACEBOY', 28, False, False))
    start_menu_fonts.append(pygame.font.SysFont('SPACEBOY', 20, False, False))

    game_fonts = []
    game_fonts.append(start_menu_fonts[0])
    game_fonts.append(start_menu_fonts[2])

    score_window_fonts = []
    score_window_fonts.append(start_menu_fonts[0])

    instruction_window_fonts = score_window_fonts

    # images laden
    screen_size = (800, 600)
    start_menu_images = []
    start_menu_images.append(util.load_image("GameScreen.jpg", screen_size))  # Hintergrund
    start_menu_images.append(util.load_image("GameScreen.jpg", (60, 60)))
    start_menu_images.append(util.load_image("GameScreen.jpg", (90, 90)))
    start_menu_images.append(util.load_image('GameScreen_2.jpg', (60, 60)))
    start_menu_images.append(util.load_image('GameScreen_2.jpg', (90, 90)))
    start_menu_images.append(util.load_image('5x5.png', (60, 60)))
    start_menu_images.append(util.load_image('5x5.png', (90, 90)))
    start_menu_images.append(util.load_image('6x6.png', (60, 60)))
    start_menu_images.append(util.load_image('6x6.png', (90, 90)))
    start_menu_images.append(util.load_image('7x7.png', (60, 60)))
    start_menu_images.append(util.load_image('7x7.png', (90, 90)))
    start_menu_images.append(util.load_image('button_the_bests.png', (80, 20)))
    start_menu_images.append(util.load_image('button_the_bests.png', (120, 30)))
    start_menu_images.append(util.load_image('button_quit.png', (40, 20)))
    start_menu_images.append(util.load_image('button_quit.png', (60, 30)))
    start_menu_images.append(util.load_image('button_instruction.png', (66, 22)))
    start_menu_images.append(util.load_image('button_instruction.png', (96, 32)))

    game_images = []
    game_images.append(util.load_image("GameScreen.jpg", screen_size))  # Hintergrund
    game_images.append(util.load_image("EndScreen.jpeg", screen_size))  # Hintergrund
    game_images.append(util.load_image('YouWon.png', (75, 100)))
    game_images.append(util.load_image('GameScreen_2.jpg', screen_size))
    game_images.append(util.load_image('bullet.png', (10, 10)))
    game_images.append(util.load_image('button_back.png', (60, 20)))
    game_images.append(util.load_image('button_back.png', (90, 30)))

    score_window_images = []
    score_window_images.append(game_images[3])
    score_window_images.append(game_images[5])
    score_window_images.append(game_images[6])

    instruction_window_images = score_window_images

    Canon.image = util.load_image('player.png', (50, 50))

    Bullet.image = game_images[4]

    img = util.load_image('Asteroid.png', (25, 25))
    Asteroid.image = img

    img = util.load_image('bullet.png', (20, 20))
    Bomb.image = img

    img = util.load_image('bomb.png', (10, 10))
    AlienBullet.image = img

    img = util.load_image('blackHole.png', (50, 50))
    BlackHole.image = img

    img = util.load_image('alien.png', (50, 50))
    Alien.image = img

    img = util.load_image('wall.jpg', (10, 10))
    Wall.image = img

    img = util.load_image('space_ship.png', (77, 55))
    SpaceShip.image = img

    img = util.load_image('Railgun.png', (10, 50))
    Decastling.image = img

    img = util.load_image('fire.png', (50, 50))
    Fire.images = [img, pygame.transform.flip(img, 1, 1)]
    Fire.image = Fire.images[0]

    # sounds laden
    game_sounds = []
    game_sounds.append(util.load_sound('bullet.wav'))
    game_sounds.append(util.load_sound('destruction.wav'))
    game_sounds.append(util.load_sound('Railgun.wav'))
    game_sounds.append(util.load_sound('blackHole.wav'))
    game_sounds.append(util.load_sound('alarm.wav'))
    game_sounds.append(util.load_sound('asteroid.wav'))

    spoken_words = {
        1: util.load_sound('round_1.wav'),
        2: util.load_sound('round_2.wav'),
        3: util.load_sound('round_3.wav'),
        "mission_completed": util.load_sound('mission_completed.wav'),
        "winner": util.load_sound('winner.wav'),
        "game_over": util.load_sound('game_over.wav'),
    }

    app = Control(screen_size)
    state_dict = {
        'start_menu': StartMenu(start_menu_images, start_menu_fonts),
        'game': Game(game_images, game_sounds, game_fonts, spoken_words),
        'score_window': ScoreWindow(score_window_images, score_window_fonts),
        'instruction_window': InstructionWindow(instruction_window_images, instruction_window_fonts)
    }

    app.setup_states(state_dict, 'start_menu')
    app.main_game_loop()
    pygame.quit()


if __name__ == '__main__':
    init_game()