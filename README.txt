Zahlen-Raten
============

Installation:
1. Flask installieren: python -m pip install flask
2. Anwendung starten: python main.py
3. Im Browser http://127.0.0.1:5000 öffnen.

Die Datei zahlenraten.db wird beim Start automatisch angelegt. Passwörter
werden als sichere Hashes gespeichert. Die Gesamtzahl der gültigen Rateversuche
wird pro Username in der Datenbank gespeichert.

Für eine sichere produktive Nutzung sollte FLASK_SECRET_KEY als Umgebungs-
variable gesetzt werden.
