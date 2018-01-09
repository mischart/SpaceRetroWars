import os, pygame, sqlite3
from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


def load_image(fileName, size=None):
    fullname = os.path.join(data_dir, fileName)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    if size:
        image = pygame.transform.scale(image, (size[0], size[1]))
    return image


class dummysound:
    def play(self): pass

def load_sound(fileName):
    if not pygame.mixer: return dummysound()
    fullname = os.path.join(data_dir, fileName)
    try:
        sound = pygame.mixer.Sound(fullname)
        return sound
    except pygame.error:
        print('Warning, unable to load, %s' % fullname)
    return dummysound()

def get_screen_rect():
    screen = pygame.display.get_surface()
    return screen.get_rect()

# /F90/ Es muss möglich sein, die Liste der besten Spielergebnisse aufzurufen (lokal).
def get_highscore_results():
    # Ich habe DB Tabelle mit Hilfe des Terminals erstellt, wie im Video 1-34: Tools -> Python Console
    # import sqlite3
    # con = sqlite3.connect('Highscore.db')
    # cursor = con.cursor()
    # cursor.execute("Create table sw (punkte varchar(32), datum varchar(32))")
    # con.commit()

    # Verbindung zu der Datenbank Highscore2, Tabelle sw
    db = sqlite3.connect('Highscore.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sw  ORDER BY -punkte")
    result = cursor.fetchall()
    db.close()
    return result