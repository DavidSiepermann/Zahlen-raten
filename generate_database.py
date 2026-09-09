import sqlite3

conn = sqlite3.connect("zahlenraten.db")
cursor = conn.cursor()

# Datenbank erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    passwort TEXT,
    rateversuche INTEGER
)
""")

conn.commit()
conn.close()