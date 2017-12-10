# Import and Initialization
import pygame
from pygame.locals import *
from canon import Canon
from bullet import Bullet

pygame.init()

pygame.mixer.music.load('data/game.mp3')
pygame.mixer.music.play(-1)

# Display
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
#size = (640, 480)
# optimal size: nächste beiden Zeilen auskommentieren und Zeile 16 löschen
size = (width, height)
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
#screen = pygame.display.set_mode(size)

pygame.display.set_caption('Space Retro Wars')

# Entities
bullet = Bullet()
canon = Canon()
spriteGroup = pygame.sprite.Group()
spriteGroup.add(canon)

bgBlue = pygame.Surface(size)
bgBlue = bgBlue.convert()
bgBlue.fill((0, 0, 139))

# Action -> Alter
# Assign Variables
keepGoing = True
clock = pygame.time.Clock()

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
                #beim Drücken der Keyup Taste erscheint das Geschoss
                spriteGroup.add(bullet)
                bullet.moveUp(spriteGroup, bullet)
            elif event.key == K_DOWN:
                #beim Drücken der KeyDown Taste wird das Spiel beendet
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
    spriteGroup.update(spriteGroup, bullet)
    spriteGroup.draw(screen)
    pygame.display.flip()
