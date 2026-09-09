# Mögliche Klassen:
# - User -> Atrribute username, rateversuche
# Methoden: registrieren, einloggen, spiel starten, 
# - Game -> Attribute gewonnen, verloren, rateversuche
# Methoden: spielen, beenden, statistik anzeigen

import flask

class User:
    def __init__(self, username, rateversuche):
        self.username = username
        self.rateversuche = rateversuche

    def registrieren(self):
        # Code zum Registrieren eines neuen Benutzers
        pass

    def einloggen(self):
        # Code zum Einloggen eines Benutzers
        pass

    def spiel_starten(self):
        # Code zum Starten eines Spiels
        pass

class Game:
    def __init__(self, gewonnen, verloren, rateversuche):
        self.gewonnen = gewonnen
        self.verloren = verloren
        self.rateversuche = rateversuche

    def spielen(self):
        # Code zum Spielen des Spiels
        pass

    def beenden(self):
        # Code zum Beenden des Spiels
        pass

    def statistik_anzeigen(self):
        # Code zum Anzeigen der Statistik
        pass

