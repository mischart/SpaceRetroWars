# Import and Initialization
import pygame, util, random
from pygame.locals import *
from alien import Alien
from AlienBullet import AlienBullet
from bullet import Bullet
from bulletAlien import BulletAlien
from canon import Canon
from wall import Wall
import sqlite3
import sys
from time import strftime


class State(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None


class StartMenu(State):
    def __init__(self, background, fonts):
        State.__init__(self)
        self.next = 'game'
        self.background = background
        self.fonts = fonts
        self.farbeaendern = 0

    def cleanup(self):
        print('cleaning up Menu state stuff')
        pygame.mixer.music.stop()

    def startup(self):
        print('starting Menu state stuff')
        # TODO checken, ob man die mp3-Datei schon früher (zusammen mit den anderen Sounds) laden kann
        pygame.mixer.music.load('data/Menue.mp3')
        pygame.mixer.music.play(-1)
        # Ich habe DB Tabelle mit Hilfe des Terminals erstellt, wie im Video 1-34: Tools -> Python Console
        # import sqlite3
        # con = sqlite3.connect('Highscore.db')
        # cursor = con.cursor()
        # cursor.execute("Create table sw (punkte varchar(32), datum varchar(32))")
        # con.commit()

        # Verbindung zu der Datenbank Highscore2, Tabelle sw
        db = sqlite3.connect('Highscore.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM sw  ORDER BY -punkte")

        # Start Screen Überschrift
        start_window_text_1 = self.fonts[0].render('SPACE', True, Color('White'))
        start_window_text_2 = self.fonts[0].render('WARS', True, Color('White'))

        screen = pygame.display.get_surface()
        screen.blit(self.background, (0, 0))
        screen.blit(start_window_text_1, [10, 10])
        screen.blit(start_window_text_2, [screen.get_width() - 250, 10])

        # Highscore Anzeige
        zeilen = 100

        # Highscore Überschrift
        start_window_highscore = self.fonts[3].render('Punkte   Erreicht am', True, Color('White'))
        screen.blit(start_window_highscore, [screen.get_width() / 3, zeilen])

        # Highscore wird aus den Zeilen der Tabelle sw aus der Datenbank Highscore2 herausgelesen und auf dem screen angezeigt
        top10 = 0
        for row in cursor:
            top10 += 1
            if top10 < 11:
                highscoreText = '    '
                for columns in range(0, 2):
                    highscoreText = highscoreText + row[columns] + '        '
                print(highscoreText)
                start_window_highscore = self.fonts[3].render(highscoreText, True, Color('White'))
                screen.blit(start_window_highscore, [screen.get_width() / 3, 25 * columns + zeilen + 10])
                zeilen += 25
        db.close()

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            print('Menu State keydown')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # TODO or Enter and close window when click on X
            # TODO: das Play-Image separat laden und dann mit playimage.get_rect().collidepoint(pygame.mouse.get_pos())
            # prüfen, ob sich der der Mause-Pointer innerhalb des Play-Images befindet
            self.done = True

    def update(self, screen):
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
        screen.blit(retro_text, [screen.get_width() / 3, screen.get_height() - 75])

    def draw(self, screen):
        pass


class Game(State):
    def __init__(self, game_images, game_sounds, game_fonts):
        State.__init__(self)
        self.next = 'start_menu'
        self.game_images = game_images
        self.game_sounds = game_sounds
        self.game_fonts = game_fonts
        self.create_sprite_groups()
        self.assign_sprite_groups()
        self.counter_for_alien_bullets = 60

    def cleanup(self):
        print('cleaning up Game state stuff')
        pygame.mixer.music.stop()
        self.canons.empty()
        self.aliens.empty()
        self.bullets.empty()
        self.aliensBullets.empty()
        self.allSprites.empty()
        self.walls.empty()

    def startup(self):
        print('starting Game state stuff')
        # TODO checken, ob man die mp3-Datei schon früher (zusammen mit den anderen Sounds) laden kann
        pygame.mixer.music.load('data/game.mp3')
        pygame.mixer.music.play(-1)
        Bullet.image = self.game_images[3]
        self.background = self.game_images[0]

        self.canon = Canon()
        # TODO: leben, punkte, als Attribute von Canon
        self.punkte = 0
        self.leben = 3
        self.game_over_setted = False
        self.create_alien_matrix()
        self.create_wall()

    def get_event(self, event):
        if event.type == QUIT:
            self.done = True
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.canon.moveRight()
            elif event.key == K_LEFT:
                self.canon.moveLeft()
            elif event.key == K_UP:
                # beim Drücken der Keyup Taste erscheint das Geschoss
                Bullet(self.canon.getPosition())
                self.game_sounds[0].play()
            elif event.key == K_DOWN:
                # beim Drücken der KeyDown Taste wird das Spiel beendet
                self.done = True
        elif event.type == KEYUP:
            # if event.key in (K_LEFT, K_RIGHT):
            pressedKeys = pygame.key.get_pressed()
            if event.key == K_LEFT:
                if not pressedKeys[K_RIGHT]:
                    self.canon.stop()
            if event.key == K_RIGHT:
                if not pressedKeys[K_LEFT]:
                    self.canon.stop()
        # TODO: Wieso??
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not self.aliens.sprites() or self.leben == 0:
                self.done = True

    def update(self, screen):
        # AlienBullets generieren
        self.counter_for_alien_bullets -= 1
        if self.counter_for_alien_bullets == 0:
            # TODO COUNTER_FOR_ALIEN_BULLETS im laufe der Zeit verringern
            self.counter_for_alien_bullets = 60
            shooting_alien = self.get_random_outer_aliens()
            if shooting_alien:
                AlienBullet(shooting_alien.getPosition())
                self.game_sounds[0].play()

        # Collisions
        self.check_collisions()

        punkteText = self.game_fonts[1].render('Punkte: ' + str(self.punkte), True, Color('White'))
        lebenText = self.game_fonts[1].render('Leben: ' + str(self.leben), True, Color('White'))
        # Redisplay
        # bgBlue.blit(charImage, charRect)  # This just makes it in the same location
        # and prints it the same size as the image
        screen.blit(self.background, (0, 0))
        screen.blit(punkteText, [screen.get_width() - 300, screen.get_height() - 50])
        screen.blit(lebenText, [50, screen.get_height() - 50])
        if self.leben == 0:
            self.background = self.game_images[1]
            self.done = True
            game_over_text = self.game_fonts[0].render('Game Over', True, Color('White'))
            screen.blit(game_over_text, [screen.get_width() / 5, 10])
            # TODO Loop Spiel wieder neu starten
        if not self.aliens.sprites():
            if not self.game_over_setted:
                self.background = self.game_images[1]
                Bullet.image = self.game_images[2]
                db = sqlite3.connect('Highscore.db')
                cursor = db.cursor()
                # Highscore Eintrag
                cursor.execute("INSERT INTO sw VALUES(?,?)", (str(self.punkte * self.leben), strftime("%d.%m.%Y")))
                db.commit()
                db.close()
                self.game_over_setted = False
            # TODO wieso? Bullet.image = you_won_image
            # Antwort von Oleg: Sei kreativ, sei abstrakt - nur so schafft man neue Gimmicks die auch etwas besonderes bieten und nicht die ewige 0815 Nummer! ;)
            you_won_text = self.game_fonts[0].render('You Won', True, Color('White'))
            screen.blit(you_won_text, [screen.get_width() / 4, screen.get_height() / 3])

        self.allSprites.update()
        # Bewegung der Alienschiffe
        if Alien.goDown:
            self.aliens.update(True)
            BulletAlien()
        Alien.goDown = False
        # Beim erreichen des unteren screen Randes wird das Spiel beendet
        # if Alien.capture:
        # keepGoing = False
        # leben -= 1
        # To Do: hier müssten jetzt die vorhandenen Aliens entweder wieder nach oben umgesetzt werden
        # oder komplett entfernt und dafür oben wiedr neue aufgebaut
        # allSprites.remove(aliens.sprites())
        # aliens.empty()
        # Alien.capture = False
        self.allSprites.draw(screen)
        pygame.display.flip()

        # Um den Game Over Bildschirm einige Zeit aufrecht zu erhalten
        if self.done and self.leben == 0:
            x = 0
            while x < 1:
                x += 1
                pygame.time.delay(1000)

    def draw(self, screen):
        screen.fill((0, 0, 255))

    def create_sprite_groups(self):
        self.canons = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.aliensBullets = pygame.sprite.Group()
        self.allSprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

    def assign_sprite_groups(self):
        Canon.groups = self.allSprites, self.canons
        Alien.groups = self.allSprites, self.aliens
        Bullet.groups = self.allSprites, self.bullets
        BulletAlien.groups = self.allSprites, self.aliensBullets
        AlienBullet.groups = self.allSprites, self.aliensBullets
        Wall.groups = self.allSprites, self.walls

    def create_alien_matrix(self):
        anzahlAliensInReihe = 5
        reihenAliens = 3
        # Erste For Schleife definiert Anzahl der Aliens Reihen und zweite for Schleife die Anzhal der Alienschiffe in der Reihe
        alienMatrix = [[Alien() for x in range(anzahlAliensInReihe)] for y in range(reihenAliens)]
        for i in range(reihenAliens):
            for j in range(anzahlAliensInReihe):
                # x Koordinaten
                alienMatrix[i][j].rect.x = 600 / 4 + j * 100
                # y Koordinaten
                alienMatrix[i][j].rect.y = i * 50
        Alien.alienMatrix = alienMatrix

    def create_wall(self):
        y = 500
        x = 150
        block_width = 70
        block_distance = 145
        for i in range(7):
            # Wall((x + i * 10, y - 10))
            # Wall((x + i * 10, y))
            # Wall((x + i * 10, y + 10))

            Wall((x + block_width + block_distance + i * 10, y - 10))
            Wall((x + block_width + block_distance + i * 10, y))
            Wall((x + block_width + block_distance + i * 10, y + 10))

            # Wall((x + (block_width + block_distance) * 2 + i * 10, y - 10))
            # Wall((x + (block_width + block_distance) * 2 + i * 10, y))
            # Wall((x + (block_width + block_distance) * 2 + i * 10, y + 10))

    def get_random_outer_aliens(self):
        last_index = len(Alien.alienMatrix) - 1
        last_row = Alien.alienMatrix[last_index]
        last_row = list(filter(lambda x: x is not None, last_row))
        if last_row:
            return random.choice(last_row)
        else:
            return None

    def check_collisions(self):
        for alien in pygame.sprite.groupcollide(self.aliens, self.bullets, 1, 1).keys():
            print("Alien.spin wäre hier noch optional möglich")
            self.game_sounds[1].play()
            self.punkte += 1

        for alien in pygame.sprite.groupcollide(self.aliens, self.walls, 1, 1).keys():
            print("Alien.spin wäre hier noch optional möglich")
            self.game_sounds[1].play()

        for bullet in pygame.sprite.groupcollide(self.aliensBullets, self.canons, 1, 0).keys():
            self.game_sounds[1].play()
            self.leben -= 1

        # TODO jetzt bekommt der Spieler auch Punkte, wenn die Kanonen-Bullets und die kleinen Bullets zusammenstoßen
        for bullet in pygame.sprite.groupcollide(self.aliensBullets, self.bullets, 1, 1).keys():
            self.game_sounds[1].play()
            self.punkte += 10
            # keepGoing = False
            # if leben == 0:
            #     keepGoing = False
            # else:
            #     keepGoing = False
            #     game(punkte, leben)

        for alien in pygame.sprite.groupcollide(self.aliens, self.canons, 1, 0).keys():
            self.game_sounds[1].play()
            self.leben -= 1
            # if leben == 0:
            #     keepGoing = False
            # else:
            #     keepGoing = False
            # game(punkte, leben)

        for wall in pygame.sprite.groupcollide(self.walls, self.bullets, 1, 1).keys():
            self.game_sounds[1].play()

        for wall in pygame.sprite.groupcollide(self.walls, self.aliensBullets, 1, 1).keys():
            self.game_sounds[1].play()


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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)

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
    start_menu_bg = util.load_image("StartScreen.jpg", screen_size)  # Hintergrund

    game_images = []
    game_images.append(util.load_image("GameScreen.jpg", screen_size))  # Hintergrund
    game_images.append(util.load_image("EndScreen.jpeg", screen_size))  # Hintergrund
    game_images.append(util.load_image('YouWon.png', (75, 100)))

    img = util.load_image('bullet.png', (10, 10))
    Bullet.image = img
    game_images.append(img)

    img = util.load_image('bomb.png', (10, 10))
    AlienBullet.image = img

    img = util.load_image('explosion1.png', (50, 50))
    BulletAlien.image = img

    img = util.load_image('Cute-spaceship-clipart-2.png', (50, 50))
    Alien.image = img

    img = util.load_image('wall.jpg', (10, 10))
    Wall.image = img

    # sounds
    game_sounds = []
    game_sounds.append(util.load_sound('bullet.wav'))
    game_sounds.append(util.load_sound('destruction.wav'))

    # Action -> Alter
    # Assign Variables
    # clock = pygame.time.Clock()
    # start_window_loop(clock, screen, fonts, backgrounds, bulletSound, destructionSound)

    app = Control(screen_size)
    state_dict = {
        'start_menu': StartMenu(start_menu_bg, start_menu_fonts),
        'game': Game(game_images, game_sounds, game_fonts)
    }

    app.setup_states(state_dict, 'start_menu')
    app.main_game_loop()
    pygame.quit()


if __name__ == '__main__':
    init_game()
