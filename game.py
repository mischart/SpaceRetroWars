# Import and Initialization
import pygame, util, random, sqlite3
from pygame.locals import *
from alien import Alien
from AlienBullet import AlienBullet
from decastling import Decastling
from bombe import Bombe
from bullet import Bullet
from asteroidenregen import Asteroidenregen
from blackHole import BlackHole
from canon import Canon
from wall import Wall
from spaceShip import SpaceShip
from time import strftime
from state import State


class Game(State):
    def __init__(self, game_images, game_sounds, game_fonts):
        State.__init__(self)
        self.next = 'start_menu'
        self.game_images = game_images
        self.game_sounds = game_sounds
        self.game_fonts = game_fonts
        self.create_sprite_groups()
        self.assign_sprite_groups()

    def cleanup(self):
        print('cleaning up Game state stuff')
        pygame.mixer.music.stop()
        self.canons.empty()
        self.aliens.empty()
        self.bullets.empty()
        self.asteroiden.empty()
        self.decastlings.empty()
        self.bombs.empty()
        self.aliensBullets.empty()
        self.allSprites.empty()
        self.walls.empty()
        self.space_ships.empty()
        self.blackHoles.empty()

    def startup(self):
        print('starting Game state stuff')
        # TODO checken, ob man die mp3-Datei schon früher (zusammen mit den anderen Sounds) laden kann
        pygame.mixer.music.load('data/game.mp3')
        pygame.mixer.music.play(-1)
        Bullet.image = self.game_images[4]
        Asteroidenregen.image = self.game_images[5]
        Bombe.image = self.game_images[6]
        if State.settings_dict['game_background'] == 1:
            self.background = self.game_images[0]
        else:
            self.background = self.game_images[3]

        # schwierigkeitsgrad = 0

        if State.settings_dict['schwierigkeitsgrad'] == 5:
            print("game.py schwierigkeitsgrad_5x5_button clicked")
            schwierigkeitsgrad = 5

        if State.settings_dict['schwierigkeitsgrad'] == 6:
            print("game.py schwierigkeitsgrad_6x6_button clicked")
            schwierigkeitsgrad = 6

        if State.settings_dict['schwierigkeitsgrad'] == 7:
            print("game.py schwierigkeitsgrad_7x7_button clicked")
            schwierigkeitsgrad = 7

        self.counter_for_alien_bullets = 60
        self.counter_for_space_ships = random.randint(200, 400)

        self.canon = Canon()
        # TODO: leben, punkte, als Attribute von Canon
        self.punkte = 0
        self.leben = 3
        self.game_over_setted = False
        self.create_alien_matrix(schwierigkeitsgrad)
        self.create_wall()

    def get_event(self, event):
        if event.type == QUIT:
            self.done = True
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.canon.moveRight()
            elif event.key == K_LEFT:
                self.canon.moveLeft()
            # /F40/ Das Spiel muss dem Spieler ermöglichen, mit der Kanone auf die Aliens zu schießen, um sie zu eliminieren. Wird ein Alien getroffen, bekommt der Spieler eine bestimmte Anzahl von Punkten.
            elif event.key == K_UP:
                if not self.bullets.sprites():
                    # beim Drücken der Keyup Taste erscheint das Geschoss
                    Bullet(self.canon.getPosition())
                    self.game_sounds[0].play()
            elif event.key == K_d:
                # beim Drücken der KeyDown Taste wird Decastling durchgeführt wenn aliens da sind und Punkte mehr als 3 vorhanden sind
                if self.aliens.sprites():
                    if self.punkte >= Decastling.price:
                        self.game_sounds[2].play()
                        Decastling(self.canon.getPosition())
                        self.punkte = self.punkte - Decastling.price
            elif event.key == K_b:
                # beim Drücken der b Taste wird Bombe abgeschossen wenn aliens da sind
                if self.aliens.sprites():
                    if not self.bombs.sprites():
                        self.game_sounds[2].play()
                        Bombe(self.canon.getPosition())
            elif event.key == K_a:
                randomPosition = random.randint(1, 800)
                screen_width = 1 * randomPosition
                asteroid_position_height = 0
                if self.aliens.sprites() or self.leben >= 0:
                    Asteroidenregen([screen_width, asteroid_position_height])
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
            if not self.aliens.sprites() or self.leben <= 0:
                self.done = True

    def update(self, screen):

        # for black hole
        # TODO Position variieren
        startPosition = (screen.get_width() / 2, 0)

        # AlienBullets generieren
        self.generate_alien_bullet()

        self.generate_space_ship()

        # Collisions
        self.check_collisions()

        # /F80/ Während des Spiels muss die Anzahl der Leben des Spielers sowie die Anzahl der erreichten Punkte dargestellt werden.
        punkteText = self.game_fonts[1].render('Punkte: ' + str(self.punkte), True, Color('White'))
        lebenText = self.game_fonts[1].render('Leben: ' + str(self.leben), True, Color('White'))
        # Redisplay
        # bgBlue.blit(charImage, charRect)  # This just makes it in the same location
        # and prints it the same size as the image
        screen.blit(self.background, (0, 0))
        screen.blit(punkteText, [screen.get_width() - 300, screen.get_height() - 50])
        screen.blit(lebenText, [50, screen.get_height() - 50])
        if self.leben <= 0:
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
                cursor.execute("INSERT INTO sw VALUES(?,?,?)",
                               (
                               str(self.punkte * self.leben), strftime("%d.%m.%Y"), State.settings_dict['player_name']))
                db.commit()
                db.close()
                self.game_over_setted = True
            # TODO wieso? Bullet.image = you_won_image
            # Antwort von Oleg: Sei kreativ, sei abstrakt - nur so schafft man neue Gimmicks die auch etwas besonderes bieten und nicht die ewige 0815 Nummer! ;)
            you_won_text = self.game_fonts[0].render('You Won', True, Color('White'))
            screen.blit(you_won_text, [screen.get_width() / 4, screen.get_height() / 3])

        self.allSprites.update()

        # Bewegung der Alienschiffe
        if Alien.goDown:
            self.aliens.update(True)
            # TODO wieso wird BlackHole mit der Position eines zufälligen, äußeren Alien verbunden?
            shooting_alien = self.get_random_outer_aliens()
            if self.aliens.sprites():
                shooting_alien_position = shooting_alien.getPosition()
                # print(screen.get_height() / 1.6, screen.get_height() / 1.4, shooting_alien_position[1])
                if screen.get_height() / 1.6 < shooting_alien_position[1] and screen.get_height() / 1.4 > \
                        shooting_alien_position[1]:
                    # BlackHole(startPosition)
                    self.game_sounds[3].play()
                    BlackHole(startPosition)
        Alien.goDown = False
        # Beim erreichen der Aliens des unteren screen Randes
        if Alien.capture:
            # keepGoing = False
            self.leben -= 1
        # allSprites.remove(aliens.sprites())
        # aliens.empty()
        # Alien.capture = False
        self.allSprites.draw(screen)
        pygame.display.flip()

        # Um den Game Over Bildschirm einige Zeit aufrecht zu erhalten
        if self.done and self.leben <= 0:
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
        self.asteroiden = pygame.sprite.Group()
        self.decastlings = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.aliensBullets = pygame.sprite.Group()
        self.allSprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.space_ships = pygame.sprite.Group()
        self.blackHoles = pygame.sprite.Group()

    def assign_sprite_groups(self):
        Canon.groups = self.allSprites, self.canons
        Alien.groups = self.allSprites, self.aliens
        Bullet.groups = self.allSprites, self.bullets
        Asteroidenregen.groups = self.allSprites, self.asteroiden
        Decastling.groups = self.allSprites, self.decastlings
        Bombe.groups = self.allSprites, self.bombs
        BlackHole.groups = self.allSprites, self.blackHoles
        AlienBullet.groups = self.allSprites, self.aliensBullets
        Wall.groups = self.allSprites, self.walls
        SpaceShip.groups = self.allSprites, self.space_ships

    def create_alien_matrix(self, schwierigkeitsgrad):
        # anzahlAliensInReihe = schwierigkeitsgrad
        # reihenAliens = schwierigkeitsgrad

        # Erste For Schleife definiert Anzahl der Aliens Reihen und zweite for Schleife die Anzhal der Alienschiffe in der Reihe
        alienMatrix = [[Alien() for x in range(schwierigkeitsgrad)] for y in range(schwierigkeitsgrad)]
        for i in range(schwierigkeitsgrad):
            for j in range(schwierigkeitsgrad):
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

    def generate_alien_bullet(self):
        # AlienBullets generieren
        self.counter_for_alien_bullets -= 1
        if self.counter_for_alien_bullets == 0:
            # TODO COUNTER_FOR_ALIEN_BULLETS im laufe der Zeit verringern
            self.counter_for_alien_bullets = 60
            shooting_alien = self.get_random_outer_aliens()
            if shooting_alien:
                AlienBullet(shooting_alien.getPosition())
                self.game_sounds[0].play()

    def generate_space_ship(self):
        if self.aliens.sprites():
            self.counter_for_space_ships -= 1
            if self.counter_for_space_ships == 0:
                self.counter_for_space_ships = random.randint(200, 400)
                SpaceShip(util.get_screen_rect().topright)

    def get_random_outer_aliens(self):
        last_index = len(Alien.alienMatrix) - 1
        last_row = Alien.alienMatrix[last_index]
        last_row = list(filter(lambda x: x is not None, last_row))
        if last_row:
            return random.choice(last_row)
        else:
            return None

    def check_collisions(self):
        for canon in pygame.sprite.groupcollide(self.canons, self.blackHoles, 1, 0).keys():
            self.game_sounds[1].play()
            self.leben -= 3

        for canon in pygame.sprite.groupcollide(self.canons, self.asteroiden, 0, 1).keys():
            self.game_sounds[1].play()
            self.leben -= 1

        for bullets in pygame.sprite.groupcollide(self.bullets, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()

        for bombs in pygame.sprite.groupcollide(self.bombs, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()

        for alien in pygame.sprite.groupcollide(self.aliens, self.bullets, 1, 1).keys():
            self.game_sounds[1].play()
            self.punkte += alien.points

        for alien in pygame.sprite.groupcollide(self.aliens, self.bombs, 1, 0).keys():
            self.game_sounds[1].play()
            self.punkte += alien.points

        for alien in pygame.sprite.groupcollide(self.aliens, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()

        for alien in pygame.sprite.groupcollide(self.aliens, self.decastlings, 1, 0).keys():
            self.game_sounds[1].play()
            self.punkte += alien.points

        for alien in pygame.sprite.groupcollide(self.aliens, self.walls, 1, 1).keys():
            self.game_sounds[1].play()

        for alien in pygame.sprite.groupcollide(self.aliens, self.blackHoles, 1, 0).keys():
            self.game_sounds[1].play()

        for bullet in pygame.sprite.groupcollide(self.aliensBullets, self.canons, 1, 0).keys():
            self.game_sounds[1].play()
            self.leben -= 1

        for aliensBullets in pygame.sprite.groupcollide(self.aliensBullets, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()

        for bombs in pygame.sprite.groupcollide(self.bombs, self.blackHoles, 1, 0).keys():
            self.game_sounds[1].play()

        for bullet in pygame.sprite.groupcollide(self.aliensBullets, self.blackHoles, 1, 0).keys():
            self.game_sounds[1].play()

        # TODO jetzt bekommt der Spieler auch Punkte, wenn die Kanonen-Bullets und die kleinen Bullets zusammenstoßen
        for alien_bullet in pygame.sprite.groupcollide(self.aliensBullets, self.bullets, 1, 1).keys():
            self.game_sounds[1].play()
            self.punkte += alien_bullet.points

        # /F30/ Wenn eine Reihe von Aliens einen unteren Bereich des Spielfeldes erreicht, verliert der Spieler eines seiner Leben.
        for alien in pygame.sprite.groupcollide(self.aliens, self.canons, 1, 0).keys():
            self.game_sounds[1].play()
            self.leben -= 1

        for wall in pygame.sprite.groupcollide(self.walls, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()

        for wall in pygame.sprite.groupcollide(self.walls, self.bullets, 1, 1).keys():
            self.game_sounds[1].play()

        for wall in pygame.sprite.groupcollide(self.walls, self.bombs, 1, 1).keys():
            self.game_sounds[1].play()

        for wall in pygame.sprite.groupcollide(self.walls, self.aliensBullets, 1, 1).keys():
            self.game_sounds[1].play()

        for wall in pygame.sprite.groupcollide(self.walls, self.blackHoles, 1, 0).keys():
            self.game_sounds[1].play()

        for space_ship in pygame.sprite.groupcollide(self.space_ships, self.bullets, 1, 1).keys():
            self.game_sounds[1].play()
            self.punkte -= space_ship.points

        for space_ship in pygame.sprite.groupcollide(self.space_ships, self.bombs, 1, 1).keys():
            self.game_sounds[1].play()

        for space_ship in pygame.sprite.groupcollide(self.space_ships, self.blackHoles, 1, 0).keys():
            self.game_sounds[1].play()

        for blackHoles in pygame.sprite.groupcollide(self.blackHoles, self.asteroiden, 0, 1).keys():
            self.game_sounds[1].play()

        for space_ship in pygame.sprite.groupcollide(self.space_ships, self.decastlings, 1, 1).keys():
            self.game_sounds[1].play()
            self.punkte += space_ship.points

        for decastlings in pygame.sprite.groupcollide(self.decastlings, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()

        for space_ship in pygame.sprite.groupcollide(self.space_ships, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()
