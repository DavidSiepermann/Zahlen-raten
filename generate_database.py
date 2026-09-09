import sqlite3

conn = sqlite3.connect("zahlenraten.db")
cursor = conn.cursor()

# Datenbank erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT NOT NULL UNIQUE,
    passwort TEXT NOT NULL,
    rateversuche INTEGER NOT NULL DEFAULT 0
)
""")

conn.commit()
conn.close()