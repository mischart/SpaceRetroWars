import gameObject


# Klasse zum Repraesentieren der Spielobjekte
# die sich bewegen koennen
class DynamicGameObject(gameObject.GameObject):
    def __init__(self, speed, midbottom=None, topright=None, center=None):
        gameObject.GameObject.__init__(self, midbottom, topright, center)
        self.speed = speed

    def update(self):
        raise NotImplementedError("Subclasses should have implemented this")
