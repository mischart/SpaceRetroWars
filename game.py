import random
from pygame.locals import *
from game_objects import *
from time import strftime
from state import State
from button import Button

LEVEL_COUNTER = 30


# Klasse mit der Spiellogik
class Game(State):
    def __init__(self, game_images, game_sounds, game_fonts, spoken_words):
        State.__init__(self)
        self.next = 'start_menu'
        self.game_images = game_images
        self.game_sounds = game_sounds
        self.game_fonts = game_fonts
        self.spoken_words = spoken_words
        self.__create_sprite_groups()
        self.__assign_sprite_groups()
        self.buttons = pygame.sprite.Group()
        self.game_over_text = self.game_fonts[0].render('Game Over', True, Color('White'))
        self.you_won_text = self.game_fonts[0].render('You Won', True, Color('White'))
        self.your_result_text = None
        Button.groups = self.buttons
        screen_size = pygame.display.get_surface().get_size()
        self.back_button = Button((game_images[5], game_images[6]),
                                  (screen_size[0] - 140, screen_size[1] - self.y_for_bottom_buttons))

        self.level_settings = {
            "current_level": 1,
            "new_level": True,
            1: {"alien_speed": 5, "bullet_counter": 60},
            2: {"alien_speed": 6, "bullet_counter": 50},
            3: {"alien_speed": 7, "bullet_counter": 40},
            "next_level_counter": LEVEL_COUNTER
        }

    def cleanup(self):
        pygame.mixer.music.stop()
        self.__empty_sprite_groups()
        self.fires.empty()
        self.walls.empty()
        self.allSprites.empty()
        self.set_buttons_to_unfocused(self.buttons)

    def startup(self):
        # TODO checken, ob man die mp3-Datei schon früher (zusammen mit den anderen Sounds) laden kann
        pygame.mixer.music.load('data/game.mp3')
        pygame.mixer.music.play(-1)
        Bullet.image = self.game_images[4]
        if State.game_settings['game_background'] == 1:
            self.background = self.game_images[0]
        else:
            self.background = self.game_images[3]

        self.canon = Canon(util.get_screen_rect().midbottom)
        self.points = 0
        self.game_over = False
        self.level_settings["current_level"] = 1
        self.level_settings["next_level_counter"] = LEVEL_COUNTER
        self.__initialize_level()

    # Level initialisieren
    def __initialize_level(self):
        self.level_settings["new_level"] = True
        level = self.level_settings["current_level"]
        bullet_counter = self.level_settings[level]["bullet_counter"]
        self.counter_for_alien_bullets = bullet_counter
        self.counter_for_space_ships = random.randint(200, 400)
        alien_speed = self.level_settings[level]["alien_speed"]
        self.__create_alien_matrix(State.game_settings['degree_of_difficulty'], alien_speed)
        self.__create_wall()
        self.number_of_asteroids_to_do = 0
        self.counter_for_asteroids = 0
        self.spoken_words[level].play()

    def __empty_sprite_groups(self):
        self.allSprites.remove(self.aliens)
        self.aliens.empty()
        self.allSprites.remove(self.bullets)
        self.bullets.empty()
        self.allSprites.remove(self.asteroiden)
        self.asteroiden.empty()
        self.allSprites.remove(self.decastlings)
        self.decastlings.empty()
        self.allSprites.remove(self.bombs)
        self.bombs.empty()
        self.allSprites.remove(self.aliensBullets)
        self.aliensBullets.empty()
        self.allSprites.remove(self.space_ships)
        self.space_ships.empty()
        self.allSprites.remove(self.blackHoles)
        self.blackHoles.empty()

    def get_event(self, event):
        if event.type == QUIT:
            self.done = True
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.canon.moveRight()
            elif event.key == K_LEFT:
                self.canon.moveLeft()
            # /F40/ Das Spiel muss dem Spieler ermöglichen, mit der Kanone auf die Aliens zu schießen, um sie zu eliminieren.
            # Wird ein Alien getroffen, bekommt der Spieler eine bestimmte Anzahl von Punkten.
            elif event.key == K_UP:
                if not self.bullets.sprites():
                    # beim Drücken der Keyup Taste erscheint das Geschoss
                    Bullet(self.canon.getPosition())
                    self.game_sounds[0].play()
            elif event.key == K_d:
                # beim Drücken der KeyDown Taste wird Decastling durchgeführt wenn aliens da sind und Punkte vorhanden sind
                if self.aliens.sprites() and self.points >= Decastling.price:
                    self.game_sounds[2].play()
                    Decastling(self.canon.getPosition())
                    self.points = self.points - Decastling.price
            elif event.key == K_s:
                # beim Drücken der s Taste wird Bombe abgeschossen wenn aliens da sind
                if self.aliens.sprites() and self.points >= Bomb.price:
                    if not self.bombs.sprites():
                        self.game_sounds[2].play()
                        Bomb(self.canon.getPosition())
                        self.points = self.points - Bomb.price
            elif event.key == K_a:
                if self.aliens.sprites() and self.points >= Asteroid.price and not self.number_of_asteroids_to_do:
                    self.number_of_asteroids_to_do = random.randint(5, 10)
                    self.points = self.points - Asteroid.price
        elif event.type == KEYUP:
            pressedKeys = pygame.key.get_pressed()
            if event.key == K_LEFT:
                if not pressedKeys[K_RIGHT]:
                    self.canon.stop()
            if event.key == K_RIGHT:
                if not pressedKeys[K_LEFT]:
                    self.canon.stop()
        elif self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.done = True
            elif event.type == pygame.MOUSEMOTION:
                self.set_buttons_to_unfocused(self.buttons)
                self.set_buttons_to_focused(self.buttons)

    def update(self, screen):
        screen.blit(self.background, (0, 0))
        # falls das Spiel noch nicht zu Ende ist
        if not self.game_over:
            # AlienBullets generieren
            self.__generate_alien_bullet()

            # SpaceShips generieren
            self.__generate_space_ship()

            # Asteroiden generieren
            self.__update_asteroid_rain()

            # Kollisionen ueberpruefen
            self.__check_collisions()

            # /F80/ Während des Spiels muss die Anzahl der Leben des Spielers sowie die Anzahl der erreichten Punkte dargestellt werden.
            punkteText = self.game_fonts[1].render('Punkte: ' + str(self.points), True, Color('White'))
            lebenText = self.game_fonts[1].render('Leben: ' + str(self.canon.lifes), True, Color('White'))
            # Redisplay
            screen.blit(punkteText, [screen.get_width() - 300, screen.get_height() - 50])
            screen.blit(lebenText, [50, screen.get_height() - 50])
            if self.canon.lifes <= 0:
                self.background = self.game_images[1]
                self.game_over = True
            if not self.aliens.sprites():
                if self.level_settings["current_level"] < 3:
                    if self.level_settings["next_level_counter"] == LEVEL_COUNTER:
                        self.spoken_words["mission_completed"].play()
                        self.__empty_sprite_groups()
                    self.level_settings["next_level_counter"] -= 1
                    if self.level_settings["next_level_counter"] < 1:
                        self.level_settings["next_level_counter"] = LEVEL_COUNTER
                        self.level_settings["current_level"] += 1
                        self.__empty_sprite_groups()
                        self.__initialize_level()
                else:
                    self.spoken_words["winner"].play()
                    self.background = self.game_images[1]
                    Bullet.image = self.game_images[2]
                    self.__empty_sprite_groups()
                    # Punkte mit Leben multiplizieren
                    result = str(self.points * self.canon.lifes)
                    # Ergebnis, Datum und Spielername in der DB speichern
                    util.save_score_result(result, strftime("%d.%m.%Y"), State.game_settings['player_name'])
                    text = '{} Leben x {} Punkte = {}'.format(self.canon.lifes, self.points, result)
                    self.your_result_text = self.game_fonts[1].render(text, True, Color('White'))
                    self.game_over = True
            self.allSprites.update()

            # Nach dem Erreichen eines Bereichs des linken bzw. des rechten Spielfeldrandes
            # werden die Reihen von Aliens um denselben Bereich nach unten verschoben
            # und die Bewegungsrichtung wird geaendert.
            if Alien.goDown:
                self.aliens.update(True)
                self.__generate_black_hole(screen)
            Alien.goDown = False

            # Beim Erreichen durch ein Alien des unteren screen Randes
            # verliert der Spieler ein Leben
            if Alien.capture:
                self.game_sounds[4].play()
                self.canon.lifes -= 1
                Alien.capture = False
        # falls das Spiel zu Ende ist
        else:
            # falls der Spieler verloren hat
            if self.canon.lifes < 1:
                screen.blit(self.game_over_text, [screen.get_width() / 5, 10])
                self.done = True
            # falls der Spieler gewonnen hat
            else:
                screen.blit(self.you_won_text, (screen.get_width() / 4, screen.get_height() / 3))
                pygame.draw.rect(screen, pygame.Color('Black'), self.bottom_menu_box)
                screen.blit(self.your_result_text, (20, screen.get_height() - 50))
                self.buttons.update()
                self.buttons.draw(screen)
            self.allSprites.update()
        self.allSprites.draw(screen)
        pygame.display.flip()

        # Um den Game Over Bildschirm einige Zeit aufrecht zu erhalten
        if self.done and self.canon.lifes < 1:
            self.spoken_words["game_over"].play()
            pygame.time.delay(2000)
        if self.level_settings["new_level"]:
            self.level_settings["new_level"] = False
            pygame.time.delay(1000)

    # Sprite-Gruppen ersellen
    def __create_sprite_groups(self):
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
        self.fires = pygame.sprite.Group()

    # Sprite-Klassen entsprechenden Sprite-Gruppen zuordnen
    def __assign_sprite_groups(self):
        Canon.groups = self.allSprites
        Alien.groups = self.allSprites, self.aliens
        Bullet.groups = self.allSprites, self.bullets
        Asteroid.groups = self.allSprites, self.asteroiden
        Decastling.groups = self.allSprites, self.decastlings
        Bomb.groups = self.allSprites, self.bombs
        BlackHole.groups = self.allSprites, self.blackHoles
        AlienBullet.groups = self.allSprites, self.aliensBullets
        Wall.groups = self.allSprites, self.walls
        SpaceShip.groups = self.allSprites, self.space_ships
        Fire.groups = self.fires, self.allSprites

    # Matrix mit Aliens erstellen
    def __create_alien_matrix(self, degree_of_difficulty, alien_speed):

        # Erste For Schleife definiert Anzahl der Aliens Reihen und zweite for Schleife die Anzhal der Alienschiffe in der Reihe
        alienMatrix = [[Alien(alien_speed) for x in range(degree_of_difficulty)] for y in range(degree_of_difficulty)]
        for i in range(degree_of_difficulty):
            for j in range(degree_of_difficulty):
                # x Koordinaten
                alienMatrix[i][j].rect.x = 600 / 4 + j * 100
                # y Koordinaten
                alienMatrix[i][j].rect.y = i * 50
        Alien.alienMatrix = alienMatrix

    # Mauer erstellen
    def __create_wall(self):
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

    # Geschosse der Aliens generieren
    def __generate_alien_bullet(self):
        # AlienBullets generieren
        self.counter_for_alien_bullets -= 1
        if self.counter_for_alien_bullets == 0:
            level = self.level_settings["current_level"]
            self.counter_for_alien_bullets = self.level_settings[level]["bullet_counter"]
            shooting_alien = self.__get_random_outer_aliens()
            if shooting_alien:
                AlienBullet(shooting_alien.getPosition())
                self.game_sounds[0].play()

    # SpaceShips generieren
    def __generate_space_ship(self):
        if self.aliens.sprites():
            self.counter_for_space_ships -= 1
            if self.counter_for_space_ships == 0:
                self.counter_for_space_ships = random.randint(200, 400)
                SpaceShip(util.get_screen_rect().topright)

    # schwarze Loecher generieren
    def __generate_black_hole(self, screen):
        if self.aliens.sprites():
            shooting_alien = self.__get_random_outer_aliens()
            shooting_alien_position = shooting_alien.getPosition()
            if screen.get_height() / 1.6 < shooting_alien_position[1] < screen.get_height() / 1.4:
                self.game_sounds[3].play()
                x = random.randint(0 + BlackHole.image.get_rect().width, screen.get_width())
                BlackHole((x, 0))

    # ein zufaelliges, aeusseres (unteres) Alien aus der Matrix bestimmen
    def __get_random_outer_aliens(self):
        last_index = len(Alien.alienMatrix) - 1
        last_row = Alien.alienMatrix[last_index]
        last_row = list(filter(lambda x: x is not None, last_row))
        if last_row:
            return random.choice(last_row)
        else:
            return None

    # Asteroidenregen generieren
    def __update_asteroid_rain(self):
        if self.number_of_asteroids_to_do > 0:
            self.counter_for_asteroids -= 1
            if self.counter_for_asteroids <= 0:
                self.counter_for_asteroids = random.randint(0, 30)
                x = random.randint(0 + Asteroid.image.get_rect().width, 800)
                Asteroid((x, 0))
                self.game_sounds[5].play()
                self.number_of_asteroids_to_do -= 1

    # Kollisionen pruefen
    def __check_collisions(self):
        for black_hole in pygame.sprite.spritecollide(self.canon, self.blackHoles, 0):
            self.game_sounds[1].play()
            self.game_sounds[4].play()
            self.canon.lifes = 0
            Fire(self.canon.rect.center)

        for asteroid in pygame.sprite.spritecollide(self.canon, self.asteroiden, 1):
            self.game_sounds[1].play()
            self.game_sounds[4].play()
            self.canon.lifes -= 1
            Fire(self.canon.rect.center)

        for bullet in pygame.sprite.groupcollide(self.bullets, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()
            Fire(bullet.rect.center)

        for bomb in pygame.sprite.groupcollide(self.bombs, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()
            Fire(bomb.rect.center)

        for alien in pygame.sprite.groupcollide(self.aliens, self.bullets, 1, 1).keys():
            self.game_sounds[1].play()
            self.points += alien.points
            Fire(alien.rect.center)

        for alien in pygame.sprite.groupcollide(self.aliens, self.bombs, 1, 0).keys():
            self.game_sounds[1].play()
            self.points += alien.points
            Fire(alien.rect.center)

        for alien in pygame.sprite.groupcollide(self.aliens, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()
            Fire(alien.rect.center)

        for alien in pygame.sprite.groupcollide(self.aliens, self.decastlings, 1, 0).keys():
            self.game_sounds[1].play()
            self.points += alien.points
            Fire(alien.rect.center)

        for alien in pygame.sprite.groupcollide(self.aliens, self.walls, 1, 1).keys():
            self.game_sounds[1].play()
            Fire(alien.rect.center)

        for alien in pygame.sprite.groupcollide(self.aliens, self.blackHoles, 1, 0).keys():
            self.game_sounds[1].play()
            Fire(alien.rect.center)

        for alien_bullet in pygame.sprite.spritecollide(self.canon, self.aliensBullets, 1):
            self.game_sounds[1].play()
            self.game_sounds[4].play()
            self.canon.lifes -= 1
            Fire(self.canon.rect.center)

        for aliensBullet in pygame.sprite.groupcollide(self.aliensBullets, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()
            Fire(aliensBullet.rect.center)

        for bomb in pygame.sprite.groupcollide(self.bombs, self.blackHoles, 1, 0).keys():
            self.game_sounds[1].play()
            Fire(bomb.rect.center)

        for bullet in pygame.sprite.groupcollide(self.aliensBullets, self.blackHoles, 1, 0).keys():
            self.game_sounds[1].play()
            Fire(bullet.rect.center)

        for alien_bullet in pygame.sprite.groupcollide(self.aliensBullets, self.bullets, 1, 1).keys():
            self.game_sounds[1].play()
            self.points += alien_bullet.points
            Fire(alien_bullet.rect.center)

        for alien in pygame.sprite.spritecollide(self.canon, self.aliens, 1):
            self.game_sounds[1].play()
            self.game_sounds[4].play()
            self.canon.lifes -= 1
            Fire(alien.rect.center)
            Fire(self.canon.rect.center)

        for wall in pygame.sprite.groupcollide(self.walls, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()
            Fire(wall.rect.center)

        for wall in pygame.sprite.groupcollide(self.walls, self.bullets, 1, 1).keys():
            self.game_sounds[1].play()
            Fire(wall.rect.center)

        for wall in pygame.sprite.groupcollide(self.walls, self.bombs, 1, 1).keys():
            self.game_sounds[1].play()
            Fire(wall.rect.center)

        for wall in pygame.sprite.groupcollide(self.walls, self.aliensBullets, 1, 1).keys():
            self.game_sounds[1].play()
            Fire(wall.rect.center)

        for wall in pygame.sprite.groupcollide(self.walls, self.blackHoles, 1, 0).keys():
            self.game_sounds[1].play()
            Fire(wall.rect.center)

        for space_ship in pygame.sprite.groupcollide(self.space_ships, self.bullets, 1, 1).keys():
            self.game_sounds[1].play()
            self.points += space_ship.points
            Fire(space_ship.rect.center)

        for space_ship in pygame.sprite.groupcollide(self.space_ships, self.bombs, 1, 1).keys():
            self.game_sounds[1].play()
            self.points += space_ship.points
            Fire(space_ship.rect.center)

        for space_ship in pygame.sprite.groupcollide(self.space_ships, self.blackHoles, 1, 0).keys():
            self.game_sounds[1].play()
            Fire(space_ship.rect.center)

        for asteroid in pygame.sprite.groupcollide(self.asteroiden, self.blackHoles, 1, 0).keys():
            self.game_sounds[1].play()
            Fire(asteroid.rect.center)

        for space_ship in pygame.sprite.groupcollide(self.space_ships, self.decastlings, 1, 1).keys():
            self.game_sounds[1].play()
            self.points += space_ship.points
            Fire(space_ship.rect.center)

        for decastlings in pygame.sprite.groupcollide(self.decastlings, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()
            Fire(decastlings.rect.center)

        for space_ship in pygame.sprite.groupcollide(self.space_ships, self.asteroiden, 1, 1).keys():
            self.game_sounds[1].play()
            Fire(space_ship.rect.center)
