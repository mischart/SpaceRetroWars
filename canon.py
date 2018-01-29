# /F20/ Das Spiel muss dem Spieler ermöglichen, am unteren Rand
# des Spielfeldes eine Kanone horizontal nach rechts und nach links zu steuern.
import dynamicGameObject

SPEED = 10


# Klasse zum Repraesentieren der Kanone,
# die von dem Spieler gesteuert wird
class Canon(dynamicGameObject.DynamicGameObject):
    def __init__(self, position):
        dynamicGameObject.DynamicGameObject.__init__(self, SPEED, midbottom=position)
        self.mode = 'stop'
        self.lifes = 3

    def update(self):
        newPos = None
        if self.mode == 'moveRight':
            newPos = self.rect.move((self.speed, 0))
        if self.mode == 'moveLeft':
            newPos = self.rect.move((-self.speed, 0))

        if newPos:
            if newPos.left >= self.screenRect.left and \
                            newPos.right <= self.screenRect.right:
                self.rect = newPos

    def getPosition(self):
        return self.rect.midtop

    def moveRight(self):
        self.mode = 'moveRight'

    def moveLeft(self):
        self.mode = 'moveLeft'

    def stop(self):
        self.mode = 'stop'
