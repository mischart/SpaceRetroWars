# -*- encodig: utf-8 -*-
___author___ = 'Kossjak'

import pygame, util

class Bird(object):  # represents the bird, not the game
    def __init__(self):
        """ The constructor of the class """
        self.image = util.load_image('bullet.png')
        # the bird's position
        self.x = 0
        self.y = 0

    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = 1 # distance moved in 1 frame, try changing it to 5
        if key[pygame.K_DOWN]: # down key
            self.y += dist # move down
        elif key[pygame.K_UP]: # up key
            self.y -= dist # move up
        if key[pygame.K_RIGHT]: # right key
            self.x += dist # move right
        elif key[pygame.K_LEFT]: # left key
            self.x -= dist # move left

    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))


pygame.init()
screen = pygame.display.set_mode((640, 400))

bird = Bird() # create an instance
clock = pygame.time.Clock()

running = True
while running:
    # handle every event since the last frame.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # quit the screen
            running = False

    bird.handle_keys() # handle the keys

    screen.fill((255,255,255)) # fill the screen with white
    bird.draw(screen) # draw the bird to the screen
    pygame.display.update() # update the screen

    clock.tick(40)