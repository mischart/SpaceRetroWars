# Import and Initialization
import pygame
from pygame.locals import *
from canon import Canon

pygame.init()

# Display
# TODO find the optimal size
size = (640, 480)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Space Retro Wars')

# Entities
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
    spriteGroup.update()
    spriteGroup.draw(screen)
    pygame.display.flip()
