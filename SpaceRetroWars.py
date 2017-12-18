# Import and Initialization
import os
import pygame, util
from pygame.locals import *
from canon import Canon
from alien import Alien
from bullet import Bullet
from bulletAliens import BulletAliens


def game(punkte, leben):

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
    BulletAliens.groups = allSprites, aliensBullets

    # Entities
    canon = Canon()

    keepGoing = True

    anzahlAliensInReihe = 5
    reihenAliens = 3

    #def erstelleAliens():
    # Erste For Schleife definiert Anzahl der Aliens Reihen und zweite for Schleife die Anzhal der Alienschiffe in der Reihe
    for i in range(reihenAliens):
        for j in range(anzahlAliensInReihe):
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

        # Collisions
        for alien in pygame.sprite.groupcollide(aliens, bullets, 1, 1).keys():
            print ("Alien.spin wäre hier noch optional möglich")
            destructionSound.play()
            punkte += 1

        for bulletAliens in pygame.sprite.groupcollide(aliensBullets, canons, 1, 1).keys():
            destructionSound.play()
            leben -= 1
            if leben == 0:
                keepGoing = False
            else:
                keepGoing = False
                game(punkte, leben)

        for alien in pygame.sprite.groupcollide(aliens, canons, 1, 1).keys():
            destructionSound.play()
            leben -= 1
            if leben == 0:
                keepGoing = False
            else:
                keepGoing = False
                game(punkte, leben)


        punkteText = font.render('Punkte: ' + str(punkte), True, (255, 255, 255))
        lebenText = font.render('Leben: ' + str(leben), True, (255, 255, 255))
        # Redisplay
        bgBlue.blit(charImage, charRect)  # This just makes it in the same location
        # and prints it the same size as the image
        screen.blit(bgBlue, (0, 0))
        screen.blit(punkteText, [aufloesungHorizontal - 300,  aufloesungVertical - 50])
        screen.blit(lebenText, [50,  aufloesungVertical - 50])
        allSprites.update()
        # Bewegung der Alienschiffe
        if Alien.goDown:
            aliens.update(True)
            aliengetPosition = (aufloesungHorizontal/2, 0)
            BulletAliens(aliengetPosition)
        Alien.goDown = False
        # Beim erreichen des unteren screen Randes wird das Spiel beendet
        #if Alien.capture:
            #keepGoing = False
            #leben -= 1
            #alien.remove()
            # To Do: hier müssten jetzt die vorhandenen Aliens entweder wieder nach oben umgesetzt werden
            # oder komplett entfernt und dafür oben wiedr neue aufgebaut
        allSprites.draw(screen)
        pygame.display.flip()
        if punkte == anzahlAliensInReihe * reihenAliens:
            print ("To Do: das Spiel muss weiter gehen, wenn die ersten Reihen abgeschossen wurden")
            keepGoing = False
            #game(punkte, leben)


if __name__ == '__main__':

    pygame.init()

    pygame.display.set_caption('Space Retro Wars')

    pygame.display.set_icon(util.load_image('LogoIcon256.jpg'))

    # Display
    font = pygame.font.SysFont('SPACEBOY', 28, True, False)
    # width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    aufloesungHorizontal = 800
    aufloesungVertical = 600
    size = (aufloesungHorizontal, aufloesungVertical)
    # screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen = pygame.display.set_mode(size)

    punkte = 0
    leben = 3

    # load images
    img = util.load_image('bullet.png', (10, 10))
    Bullet.image = img

    img = util.load_image('explosion1.png', (50, 50))
    BulletAliens.image = img

    img = util.load_image('Cute-spaceship-clipart-2.png', (50, 50))
    Alien.image = img

    # sounds
    pygame.mixer.music.load('data/game.mp3')
    pygame.mixer.music.play(-1)
    bulletSound = util.load_sound('bullet.wav')
    destructionSound = util.load_sound('destruction.wav')

    # Hintergrund
    bgBlue = pygame.Surface(size)
    bgBlue = bgBlue.convert()
    bgBlue.fill((0, 0, 139))

    charRect = pygame.Rect((0, 0), (aufloesungHorizontal, aufloesungVertical))
    #print os.path.abspath("airbender.png")
    charImage = pygame.image.load(os.path.abspath("data/StartScreen.jpg"))
    charImage = pygame.transform.scale(charImage, charRect.size)
    charImage = charImage.convert()

    # Action -> Alter
    # Assign Variables
    clock = pygame.time.Clock()

    game(punkte, leben)