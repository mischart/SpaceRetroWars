# Import and Initialization
import pygame, util
from alien import Alien
from AlienBullet import AlienBullet
from railgun import Railgun
from bullet import Bullet
from blackHole import BlackHole
from wall import Wall
from spaceShip import SpaceShip
from game import Game
from start_menu import StartMenu


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

    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous

    def update(self):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen)

    def event_loop(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)
        if self.state.active_text_input:
            self.state.get_events_to_text_input(events)

    def main_game_loop(self):
        while not self.done:
            self.clock.tick(30)
            self.event_loop()
            self.update()
            pygame.display.flip()


def init_game():
    pygame.init()
    # load fonts
    # TODO : change Lists to Dictionaries
    start_menu_fonts = []
    start_menu_fonts.append(pygame.font.SysFont('SPACEBOY', 56, False, False))
    start_menu_fonts.append(pygame.font.SysFont('Space Cruiser', 56, False, True))
    start_menu_fonts.append(pygame.font.SysFont('SPACEBOY', 28, True, False))
    start_menu_fonts.append(pygame.font.SysFont('SPACEBOY', 20, False, False))

    game_fonts = []
    game_fonts.append(pygame.font.SysFont('SPACEBOY', 56, True, False))
    game_fonts.append(pygame.font.SysFont('SPACEBOY', 28, True, False))

    # load images
    screen_size = (800, 600)
    start_menu_images = []
    start_menu_images.append(util.load_image("StartScreen.jpg", screen_size))  # Hintergrund
    start_menu_images.append(util.load_image("GameScreen.jpg", (60, 60)))
    start_menu_images.append(util.load_image("GameScreen.jpg", (90, 90)))
    start_menu_images.append(util.load_image('GameScreen_2.jpg', (60, 60)))
    start_menu_images.append(util.load_image('GameScreen_2.jpg', (90, 90)))
    start_menu_images.append(util.load_image('Play.png', (60, 60)))
    start_menu_images.append(util.load_image('Play.png', (90, 90)))

    game_images = []
    game_images.append(util.load_image("GameScreen.jpg", screen_size))  # Hintergrund
    game_images.append(util.load_image("EndScreen.jpeg", screen_size))  # Hintergrund
    game_images.append(util.load_image('YouWon.png', (75, 100)))
    game_images.append(util.load_image('GameScreen_2.jpg', screen_size))

    img = util.load_image('bullet.png', (10, 10))
    Bullet.image = img
    game_images.append(img)

    img = util.load_image('bomb.png', (10, 10))
    AlienBullet.image = img

    img = util.load_image('blackHole.png', (50, 50))
    BlackHole.image = img

    img = util.load_image('Cute-spaceship-clipart-2.png', (50, 50))
    Alien.image = img

    img = util.load_image('wall.jpg', (10, 10))
    Wall.image = img

    img = util.load_image('space_ship.png', (77, 55))
    SpaceShip.image = img

    img = util.load_image('Railgun.png', (10, 50))
    Railgun.image = img

    # sounds
    game_sounds = []
    game_sounds.append(util.load_sound('bullet.wav'))
    game_sounds.append(util.load_sound('destruction.wav'))
    game_sounds.append(util.load_sound('Railgun.wav'))
    game_sounds.append(util.load_sound('blackHole.wav'))

    # Action -> Alter
    # Assign Variables
    # clock = pygame.time.Clock()
    # start_window_loop(clock, screen, fonts, backgrounds, bulletSound, destructionSound)

    app = Control(screen_size)
    state_dict = {
        'start_menu': StartMenu(start_menu_images, start_menu_fonts),
        'game': Game(game_images, game_sounds, game_fonts)
    }

    app.setup_states(state_dict, 'start_menu')
    app.main_game_loop()
    pygame.quit()


if __name__ == '__main__':
    init_game()
