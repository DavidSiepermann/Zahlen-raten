import os
import random
import sqlite3
from functools import wraps
from contextlib import contextmanager

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "zahlenraten.db")
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")


@contextmanager
def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db():
    with get_db() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT NOT NULL UNIQUE,
                passwort TEXT NOT NULL,
                rateversuche INTEGER NOT NULL DEFAULT 0
            )
            """
        )


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            flash("Bitte melde dich zuerst an.", "error")
            return redirect(url_for("index"))
        return view(*args, **kwargs)

    return wrapped_view


def start_new_game():
    session["zielzahl"] = random.randint(0, 100)
    session["spielversuche"] = 0
    session["spiel_beendet"] = False


@app.route("/", methods=["GET", "POST"])
def index():
    if "username" in session:
        return redirect(url_for("spiel"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        action = request.form.get("action")
        if not username or not password:
            flash("Username und Passwort sind erforderlich.", "error")
            return render_template("index.html")

        if action == "register":
            with get_db() as connection:
                existing_user = connection.execute(
                    "SELECT 1 FROM users WHERE username = ?", (username,)
                ).fetchone()
                if existing_user:
                    flash("Dieser Username ist bereits vergeben.", "error")
                else:
                    connection.execute(
                        "INSERT INTO users (username, passwort, rateversuche) VALUES (?, ?, 0)",
                        (username, generate_password_hash(password)),
                    )
                    flash("Registrierung erfolgreich. Du kannst dich jetzt anmelden.", "success")
            return render_template("index.html")

        if action == "login":
            with get_db() as connection:
                user = connection.execute(
                    "SELECT username, passwort FROM users WHERE username = ?", (username,)
                ).fetchone()
            if user and check_password_hash(user["passwort"], password):
                session.clear()
                session["username"] = user["username"]
                start_new_game()
                return redirect(url_for("spiel"))
            flash("Username oder Passwort ist falsch.", "error")

    return render_template("index.html")


@app.route("/spiel", methods=["GET", "POST"])
@login_required
def spiel():
    if "zielzahl" not in session:
        start_new_game()
    username = session["username"]
    message = None
    message_type = None

    if request.method == "POST":
        action = request.form.get("action")
        if action == "new_game":
            start_new_game()
            flash("Ein neues Spiel wurde gestartet.", "success")
            return redirect(url_for("spiel"))
        if action == "guess" and not session.get("spiel_beendet"):
            raw_guess = request.form.get("guess", "").strip()
            try:
                guess = int(raw_guess)
            except ValueError:
                message = "Bitte gib eine ganze Zahl zwischen 0 und 100 ein."
                message_type = "error"
            else:
                if not 0 <= guess <= 100:
                    message = "Deine Zahl muss zwischen 0 und 100 liegen."
                    message_type = "error"
                else:
                    session["spielversuche"] = session.get("spielversuche", 0) + 1
                    with get_db() as connection:
                        connection.execute(
                            "UPDATE users SET rateversuche = rateversuche + 1 WHERE username = ?",
                            (username,),
                        )
                    if guess == session["zielzahl"]:
                        session["spiel_beendet"] = True
                        message = f"Richtig! Die gesuchte Zahl war {guess}."
                        message_type = "success"
                    elif session["spielversuche"] >= 3:
                        session["spiel_beendet"] = True
                        message = f"Das Spiel ist vorbei. Die gesuchte Zahl war {session['zielzahl']}."
                        message_type = "error"
                    elif guess < session["zielzahl"]:
                        message = "Zu niedrig. Versuch es noch einmal!"
                        message_type = "error"
                    else:
                        message = "Zu hoch. Versuch es noch einmal!"
                        message_type = "error"

    with get_db() as connection:
        user = connection.execute(
            "SELECT rateversuche FROM users WHERE username = ?", (username,)
        ).fetchone()
    return render_template(
        "spiel.html",
        username=username,
        message=message,
        message_type=message_type,
        spielversuche=session.get("spielversuche", 0),
        spiel_beendet=session.get("spiel_beendet", False),
        gesamtversuche=user["rateversuche"],
    )


@app.route("/logout")
def logout():
    session.clear()
    flash("Du wurdest ausgeloggt.", "success")
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
