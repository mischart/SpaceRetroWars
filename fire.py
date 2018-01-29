import gameObject

START_LIFES = 12


# Klasse zum Repraesentieren des Feuers nach der Explosion
class Fire(gameObject.GameObject):
    images = None
    animation_cycle = 3

    def __init__(self, center):
        gameObject.GameObject.__init__(self, center=center)
        self.lifes = START_LIFES

    def update(self):
        self.lifes = self.lifes - 1
        self.image = self.images[self.lifes // self.animation_cycle % 2]
        if self.lifes <= 0: self.kill()
