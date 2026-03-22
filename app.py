from flask import Flask, render_template
from flask_socketio import SocketIO, send
import random

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

ADMIN_USER = "Liam"

def is_admin(user):
    return user == ADMIN_USER

# =============================
# SYSTEM SETTINGS
# =============================
ori_enabled = True
morse_enabled = True
morse_chance = 0.25

# =============================
# MORSE CODE
# =============================
MORSE_CODE = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.',
    'f': '..-.', 'g': '--.', 'h': '....', 'i': '..', 'j': '.---',
    'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---',
    'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-',
    'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--',
    'z': '--..',
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.',
    ' ': '/'
}

def to_morse(text):
    return ' '.join(MORSE_CODE.get(c.lower(), '') for c in text)

# =============================
# ROUTES
# =============================
@app.route("/")
def index():
    return render_template("index.html")

# =============================
# SOCKET
# =============================
@socketio.on("message")
def handle_message(data):
    global ori_enabled, morse_enabled, morse_chance

    user = data.get("user")
    text = data.get("text")

    # ===== ADMIN CONTROLS =====
    if is_admin(user):

        if text == "//ori_on":
            ori_enabled = True
            send({"user":"System","text":"🟢 Ori ON"}, broadcast=True)
            return

        if text == "//ori_off":
            ori_enabled = False
            send({"user":"System","text":"🔴 Ori OFF"}, broadcast=True)
            return

        if text == "//morse_on":
            morse_enabled = True
            send({"user":"System","text":"📡 Morse ON"}, broadcast=True)
            return

        if text == "//morse_off":
            morse_enabled = False
            send({"user":"System","text":"📡 Morse OFF"}, broadcast=True)
            return

        if text.startswith("//morse_level"):
            try:
                morse_chance = float(text.split(" ")[1])
            except:
                pass
            return

        if text.startswith("//ori_say"):
            msg = text.replace("//ori_say","").strip()
            send({"user":"Ori","text":msg}, broadcast=True)
            return

        if text.startswith("//ori_morse"):
            msg = text.replace("//ori_morse","").strip()
            send({"user":"Ori","text":to_morse(msg)}, broadcast=True)
            return

        if text == "//ori_alert":
            send({"user":"System","text":"⚠️ SYSTEM ALERT"}, broadcast=True)
            return

        if text == "//ori_glitch":
            send({"user":"System","text":"💥 GLITCH"}, broadcast=True)
            return

    # ===== NORMAL MESSAGE =====
    send({"user":user,"text":text}, broadcast=True)

    # ===== ORI RANDOM =====
    if ori_enabled and random.random() < 0.15:
        send({"user":"Ori","text":"👁️ Watching..."}, broadcast=True)

    # ===== MORSE =====
    if ori_enabled and morse_enabled and random.random() < morse_chance:
        send({
            "user":"Ori",
            "text":"📡 " + to_morse(text)
        }, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
