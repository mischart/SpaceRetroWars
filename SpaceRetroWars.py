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
    fontStartgame = pygame.font.SysFont('SPACEBOY', 56, False, False)
    fontStartgame2 = pygame.font.SysFont('Space Cruiser', 56, False, True)
    startgame = fontStartgame.render('RETRO', True, Color('White'))
    startgame2 = fontStartgame2.render('SPACE', True, Color('White'))
    startgame3 = fontStartgame2.render('WARS', True, Color('White'))
    # width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    aufloesungHorizontal = 800
    aufloesungVertical = 600
    screen_size = (aufloesungHorizontal, aufloesungVertical)
    # screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen = pygame.display.set_mode(screen_size)

    # load images
    gamescreen = util.load_image("GameScreen.jpg", screen_size)  # Hintergrund
    background = util.load_image("StartScreen.jpg", screen_size)  # Hintergrund
    background = background.convert()

    img = util.load_image('bullet.png', (10, 10))
    Bullet.image = img

    img = util.load_image('bomb.png', (10, 10))
    AlienBullet.image = img

    img = util.load_image('explosion1.png', (50, 50))
    BulletAlien.image = img

    img = util.load_image('Cute-spaceship-clipart-2.png', (50, 50))
    Alien.image = img

    screen.blit(background, (0, 0))
    screen.blit(startgame2, [10, 10])
    screen.blit(startgame3, [screen_size[0] - 250, 10])

    # sounds
    pygame.mixer.music.load('data/game.mp3')
    pygame.mixer.music.play(-1)
    bulletSound = util.load_sound('bullet.wav')
    destructionSound = util.load_sound('destruction.wav')

    # Action -> Alter
    # Assign Variables
    clock = pygame.time.Clock()

    startmenue = True
    farbeaendern = 0
    while startmenue:
        farbeaendern += 1
        if farbeaendern == 150:
            startgame = fontStartgame.render('RETRO', True, Color('Red'))
        if farbeaendern == 300:
            startgame = fontStartgame.render('RETRO', True, Color('Green'))
        if farbeaendern == 450:
            startgame = fontStartgame.render('RETRO', True, Color('Blue '))
        if farbeaendern == 600:
            startgame = fontStartgame.render('RETRO', True, Color('Cyan'))
        if farbeaendern == 750:
            startgame = fontStartgame.render('RETRO', True, Color('Magenta'))
        if farbeaendern == 900:
            startgame = fontStartgame.render('RETRO', True, Color('Yellow'))
        #if farbeaendern == 1050:
            #startgame = fontStartgame.render('RETRO', True, Color('Black'))
        #if farbeaendern == 1200:
            #startgame = fontStartgame.render('RETRO', True, Color('Orange'))
        #if farbeaendern == 1350:
            #startgame = fontStartgame.render('RETRO', True, Color('Violet'))
        #if farbeaendern == 1500:
            #startgame = fontStartgame.render('RETRO', True, Color('Purple'))
        #if farbeaendern == 1650:
            #startgame = fontStartgame.render('RETRO', True, Color('Brown'))
        #if farbeaendern == 1800:
            #startgame = fontStartgame.render('RETRO', True, Color('Grey'))
        #if farbeaendern == 1950:
            #startgame = fontStartgame.render('RETRO', True, Color('Pink'))
        #if farbeaendern == 2100:
            #startgame = fontStartgame.render('RETRO', True, Color('Beige'))
        #if farbeaendern == 2250:
            #startgame = fontStartgame.render('RETRO', True, Color('Gold'))
        #if farbeaendern == 2400:
            #startgame = fontStartgame.render('RETRO', True, Color('Turquoise'))
        #if farbeaendern == 2550:
            #startgame = fontStartgame.render('RETRO', True, Color('Maroon'))
        #if farbeaendern == 2700:
            #startgame = fontStartgame.render('RETRO', True, Color('Khaki'))
            farbeaendern = 0
        print (farbeaendern)
        screen.blit(startgame, [screen_size[0] / 3, screen_size[1] - 75])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                startmenue = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                background = gamescreen
                startmenue = False
                game_loop(screen, background, clock, bulletSound, destructionSound, font)
                # Set the x, y postions of the mouse click
                #x, y = event.pos
                #if ball.get_rect().collidepoint(x, y):
            # do swap
        pygame.display.update()


def game_loop(screen, charImage, clock, bulletSound, destructionSound, font):

    counter_for_alien_bullets = COUNTER_FOR_ALIEN_BULLETS
    punkte = 0
    leben = 3
    keepGoing = True
    screen_size = (screen.get_width(), screen.get_height())

    # Fürs Spielende
    endscreen = util.load_image("EndScreen.jpeg", screen_size)  # Hintergrund
    fontgameOver = pygame.font.SysFont('SPACEBOY', 56, True, False)
    gameOver = fontgameOver.render('Game Over', True, Color('White'))
    imgYouWon = util.load_image('YouWon.png', (75, 100))

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not aliens.sprites() or leben == 0:
                    keepGoing = False

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
        if leben == 0:
            charImage = endscreen
            screen.blit(gameOver, [screen_size[0] / 5, 10])
            keepGoing = False
        if not aliens.sprites():
            charImage = endscreen
            gameOver = fontgameOver.render('You Won', True, Color('White'))
            Bullet.image = imgYouWon
            screen.blit(gameOver, [screen_size[0] / 4, screen_size[1] / 3])
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

        # Um den Game Over Bildschirm einige Zeit aufrecht zu erhalten
        x = 0
        if keepGoing == False:
            while x < 1:
                x += 1
                pygame.time.delay(1000)


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