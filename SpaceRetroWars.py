# Import and Initialization
import pygame, util
from pygame.locals import *
from canon import Canon
from alien import Alien
from bullet import Bullet


def game():
    pygame.init()

    pygame.display.set_caption('Space Retro Wars')

    pygame.display.set_icon(util.load_image('LogoIcon256.jpg'))

    pygame.mixer.music.load('data/game.mp3')
    pygame.mixer.music.play(-1)

    # Display
    # width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    aufloesungHorizontal = 800
    aufloesungVertical = 600
    size = (aufloesungHorizontal, aufloesungVertical)
    # screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen = pygame.display.set_mode(size)

    # load images
    img = util.load_image('bullet.png', (10, 10))
    Bullet.image = img

    img = util.load_image('Cute-spaceship-clipart-2.png', (50, 50))
    Alien.image = img

    # sprite groups
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    allSprites = pygame.sprite.Group()

    # assign sprite groups to sprites
    Canon.groups = allSprites
    Alien.groups = allSprites, aliens
    Bullet.groups = allSprites, bullets

    # Entities
    canon = Canon()

    bgBlue = pygame.Surface(size)
    bgBlue = bgBlue.convert()
    bgBlue.fill((0, 0, 139))

    # Action -> Alter
    # Assign Variables
    keepGoing = True
    clock = pygame.time.Clock()

    anzahlAliens = 5
    reihenAliens = 3

    # Erste For Schleife definiert Anzahl der Aliens Reihen und zweite for Schleife die Anzhal der Alienschiffe in der Reihe
    for i in range(reihenAliens):
        for j in range(anzahlAliens):
            alien = Alien()
            # x Koordinaten
            alien.rect.x = aufloesungVertical / 4 + j * 100
            # y Koordinaten
            alien.rect.y = i * 50
            # alien sprite zu enemy list hinzufügen
            # aliens.add(alien)
            # dies brauchen wir nicht wegen: Alien.groups = allSprites, aliens

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

        # Redisplay
        screen.blit(bgBlue, (0, 0))
        allSprites.update()
        if Alien.goDown:
            aliens.update(True)
        Alien.goDown = False
        if Alien.capture:
            keepGoing = False
        allSprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    game()