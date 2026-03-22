from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import random
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

ADMIN_USER = "Liam"

ori_enabled = True
morse_enabled = True
morse_chance = 0.25

MORSE_CODE = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.',
    'f': '..-.', 'g': '--.', 'h': '....', 'i': '..',
    'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--',
    'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-',
    'r': '.-.', 's': '...', 't': '-', 'u': '..-',
    'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--',
    'z': '--..', ' ': '/'
}

def to_morse(text):
    return ' '.join(MORSE_CODE.get(c.lower(), '') for c in text)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("typing")
def typing(data):
    emit("typing", data, broadcast=True)

@socketio.on("message")
def handle_message(data):
    global ori_enabled, morse_enabled, morse_chance

    user = data["user"]
    text = data["text"]

    send({"user": user, "text": text}, broadcast=True)

    # ORI thinking effect
    if ori_enabled and random.random() < 0.2:
        emit("typing", {"user": "Ori"}, broadcast=True)
        time.sleep(1.5)

        send({"user": "Ori", "text": "👁️ I'm watching..."}, broadcast=True)

    # MORSE
    if ori_enabled and morse_enabled and random.random() < morse_chance:
        send({"user": "Ori", "text": "📡 " + to_morse(text)}, broadcast=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
