# diverse Hilfsfunktionen

import os, pygame, sqlite3
from pygame.compat import geterror

db_file_name = 'Highscore.db'
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
# lesender Zugriff auf die DB
def get_highscore_results():
    # Verbindung zu der Datenbank Highscore2, Tabelle sw
    db = sqlite3.connect(db_file_name)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sw  ORDER BY -punkte")
    result = cursor.fetchall()
    db.close()
    return result


# schreibender Zugriff auf die DB zum Speichern der Spielerergebnisse
def save_score_result(result, date, name):
    db = sqlite3.connect(db_file_name)
    cursor = db.cursor()
    # Highscore Eintrag
    cursor.execute("INSERT INTO sw VALUES(?,?,?)",
                   (result, date, name))
    db.commit()
    db.close()
