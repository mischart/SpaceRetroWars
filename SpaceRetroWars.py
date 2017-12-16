# Import and Initialization
import pygame, util
from pygame.locals import *
from canon import Canon
from aliens import Aliens
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
    # optimal size: nächste beiden Zeilen auskommentieren und Zeile 16 löschen
    # size = (width, height)
    # screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen = pygame.display.set_mode(size)

    # load images
    img = util.load_image('bullet.png')
    img = pygame.transform.scale(img, (10, 10))
    Bullet.image = img

    # sprite groups
    aliens_liste = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    allSprites = pygame.sprite.Group()

    # assign sprite groups to sprites
    Canon.groups = allSprites
    Aliens.groups = allSprites
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
            aliens = Aliens()
            # x Koordinaten
            aliens.rect.x = aufloesungVertical/4 + j * 100
            # y Koordinaten
            aliens.rect.y = i * 50
            # alien sprite zu enemy list hinzufügen
            aliens_liste.add(aliens)

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
                    #aliens.moveRight()
                elif event.key == K_LEFT:
                    canon.moveLeft()
                    #aliens.moveLeft()
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
                        #aliens.stop()
                if event.key == K_RIGHT:
                    if not pressedKeys[K_LEFT]:
                        canon.stop()
                        #aliens.stop()

        # Redisplay
        screen.blit(bgBlue, (0, 0))
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    game()