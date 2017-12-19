# Import and Initialization
import pygame, util, random
from pygame.locals import *
from canon import Canon
from alien import Alien
from bullet import Bullet
from bulletAlien import BulletAlien
from AlienBullet import AlienBullet

# game constants
COUNTER_FOR_ALIEN_BULLETS = 60


def init_game():
    pygame.init()

    pygame.display.set_caption('Space Retro Wars')

    pygame.display.set_icon(util.load_image('LogoIcon256.jpg'))

    # Display
    font = pygame.font.SysFont('SPACEBOY', 28, True, False)
    # width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    aufloesungHorizontal = 800
    aufloesungVertical = 600
    screen_size = (aufloesungHorizontal, aufloesungVertical)
    # screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen = pygame.display.set_mode(screen_size)

    # load images
    background = util.load_image("StartScreen.jpg", screen_size)  # Hintergrund
    background = background.convert()

    img = util.load_image('bullet.png', (10, 10))
    Bullet.image = img
    AlienBullet.image = img

    img = util.load_image('explosion1.png', (50, 50))
    BulletAlien.image = img

    img = util.load_image('Cute-spaceship-clipart-2.png', (50, 50))
    Alien.image = img

    # sounds
    pygame.mixer.music.load('data/game.mp3')
    pygame.mixer.music.play(-1)
    bulletSound = util.load_sound('bullet.wav')
    destructionSound = util.load_sound('destruction.wav')

    # Action -> Alter
    # Assign Variables
    clock = pygame.time.Clock()

    game_loop(screen, background, clock, bulletSound, destructionSound, font)


def game_loop(screen, charImage, clock, bulletSound, destructionSound, font):
    counter_for_alien_bullets = COUNTER_FOR_ALIEN_BULLETS
    punkte = 0
    leben = 3
    keepGoing = True
    screen_size = (screen.get_width(), screen.get_height())

    # sprite groups
    canons = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    aliensBullets = pygame.sprite.Group()
    allSprites = pygame.sprite.Group()

    # assign sprite groups to sprites
    Canon.groups = allSprites, canons
    Alien.groups = allSprites, aliens
    Bullet.groups = allSprites, bullets
    BulletAlien.groups = allSprites, aliensBullets
    AlienBullet.groups = allSprites, aliensBullets

    # Entities
    canon = Canon()

    anzahlAliensInReihe = 5
    reihenAliens = 3

    # def erstelleAliens():
    # Erste For Schleife definiert Anzahl der Aliens Reihen und zweite for Schleife die Anzhal der Alienschiffe in der Reihe
    alienMatrix = [[Alien() for x in range(anzahlAliensInReihe)] for y in range(reihenAliens)]
    Alien.alienMatrix = alienMatrix
    for i in range(reihenAliens):
        for j in range(anzahlAliensInReihe):
            # x Koordinaten
            alienMatrix[i][j].rect.x = screen_size[1] / 4 + j * 100
            # y Koordinaten
            alienMatrix[i][j].rect.y = i * 50

    # Loop
    while keepGoing:
        # Timer
        clock.tick(30)
        # Event Handling
        for event in pygame.event.get():
            if event.type == QUIT:
                keepGoing = False
                break
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    canon.moveRight()
                elif event.key == K_LEFT:
                    canon.moveLeft()
                elif event.key == K_UP:
                    # beim Drücken der Keyup Taste erscheint das Geschoss
                    Bullet(canon.getPosition())
                    bulletSound.play()
                elif event.key == K_DOWN:
                    # beim Drücken der KeyDown Taste wird das Spiel beendet
                    keepGoing = False
            elif event.type == KEYUP:
                # if event.key in (K_LEFT, K_RIGHT):
                pressedKeys = pygame.key.get_pressed()
                if event.key == K_LEFT:
                    if not pressedKeys[K_RIGHT]:
                        canon.stop()
                if event.key == K_RIGHT:
                    if not pressedKeys[K_LEFT]:
                        canon.stop()

        # AlienBullets generieren
        counter_for_alien_bullets -= 1
        if counter_for_alien_bullets == 0:
            # TODO COUNTER_FOR_ALIEN_BULLETS im laufe der Zeit verringern
            counter_for_alien_bullets = COUNTER_FOR_ALIEN_BULLETS
            shooting_alien = get_random_outer_Aliens(alienMatrix)
            if shooting_alien:
                AlienBullet(shooting_alien.getPosition())
                bulletSound.play()

        # Collisions
        for alien in pygame.sprite.groupcollide(aliens, bullets, 1, 1).keys():
            print("Alien.spin wäre hier noch optional möglich")
            destructionSound.play()
            punkte += 1

        for bulletAliens in pygame.sprite.groupcollide(aliensBullets, canons, 1, 0).keys():
            destructionSound.play()
            leben -= 1
            # keepGoing = False
            # if leben == 0:
            #     keepGoing = False
            # else:
            #     keepGoing = False
            #     game(punkte, leben)

        for alien in pygame.sprite.groupcollide(aliensBullets, bullets, 1, 1).keys():
            destructionSound.play()
            punkte += 10
            # keepGoing = False
            # if leben == 0:
            #     keepGoing = False
            # else:
            #     keepGoing = False
            #     game(punkte, leben)

        for alien in pygame.sprite.groupcollide(aliens, canons, 1, 0).keys():
            destructionSound.play()
            leben -= 1
            # if leben == 0:
            #     keepGoing = False
            # else:
            #     keepGoing = False
            # game(punkte, leben)

        punkteText = font.render('Punkte: ' + str(punkte), True, Color('White'))
        lebenText = font.render('Leben: ' + str(leben), True, Color('White'))
        # Redisplay
        # bgBlue.blit(charImage, charRect)  # This just makes it in the same location
        # and prints it the same size as the image
        screen.blit(charImage, (0, 0))
        screen.blit(punkteText, [screen_size[0] - 300, screen_size[1] - 50])
        screen.blit(lebenText, [50, screen_size[1] - 50])
        allSprites.update()
        # Bewegung der Alienschiffe
        if Alien.goDown:
            aliens.update(True)
            aliengetPosition = (screen_size[0] / 2, 0)
            BulletAlien(aliengetPosition)
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
        allSprites.draw(screen)
        pygame.display.flip()
        if not aliens.sprites() or leben == 0:
            print("To Do: das Spiel muss weiter gehen, wenn die ersten Reihen abgeschossen wurden")
            keepGoing = False
            # game(punkte, leben)


def get_random_outer_Aliens(alienMatrix):
    last_index = len(alienMatrix) - 1
    last_row = alienMatrix[last_index]
    last_row = list(filter(lambda x: x is not None, last_row))
    if last_row:
        return random.choice(last_row)
    else:
        return None


if __name__ == '__main__':
    init_game()