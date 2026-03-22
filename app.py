from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, send, emit
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# USERS (LOGIN)
users = {
    "Liam": {"password": "Z7!qP2@vLm#8Xr", "admin": True},
    "Carter": {"password": "B4$kT9^nW2*eQh", "admin": False}
}

# SYSTEM STATES
ori_enabled = True
morse_enabled = True
morse_chance = 0.25

# MORSE CODE
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

# LOGIN PAGE
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["user"] = username
            session["admin"] = users[username]["admin"]
            return redirect("/chat")

    return render_template("login.html")

# CHAT PAGE
@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect("/")
    return render_template(
        "index.html",
        user=session["user"],
        admin=session["admin"]
    )

# TYPING INDICATOR
@socketio.on("typing")
def typing(data):
    emit("typing", data, broadcast=True)

# CHAT SYSTEM
@socketio.on("message")
def handle_message(data):
    global ori_enabled, morse_enabled, morse_chance

    user = data.get("user")
    text = data.get("text")
    is_admin = data.get("admin")

    # SEND NORMAL MESSAGE
    send({"user": user, "text": text}, broadcast=True)

    # ADMIN CONTROLS
    if is_admin:
        if text == "//ori_on":
            ori_enabled = True
            send({"user": "System", "text": "🟢 Ori ON"}, broadcast=True)
            return

        if text == "//ori_off":
            ori_enabled = False
            send({"user": "System", "text": "🔴 Ori OFF"}, broadcast=True)
            return

        if text == "//morse_on":
            morse_enabled = True
            send({"user": "System", "text": "📡 Morse ON"}, broadcast=True)
            return

        if text == "//morse_off":
            morse_enabled = False
            send({"user": "System", "text": "📡 Morse OFF"}, broadcast=True)
            return

        if text.startswith("//morse_level"):
            try:
                morse_chance = float(text.split(" ")[1])
                send({"user": "System", "text": f"Morse level: {morse_chance}"}, broadcast=True)
            except:
                pass
            return

        if text.startswith("//ori_say"):
            msg = text.replace("//ori_say", "").strip()
            send({"user": "Ori", "text": msg}, broadcast=True)
            return

        if text.startswith("//ori_morse"):
            msg = text.replace("//ori_morse", "").strip()
            send({"user": "Ori", "text": to_morse(msg)}, broadcast=True)
            return

    # ORI RANDOM BEHAVIOR
    if ori_enabled and random.random() < 0.2:
        emit("typing", {"user": "Ori"}, broadcast=True)
        send({"user": "Ori", "text": "👁️ I'm watching..."}, broadcast=True)

    # MORSE RANDOM
    if ori_enabled and morse_enabled and random.random() < morse_chance:
        send({"user": "Ori", "text": "📡 " + to_morse(text)}, broadcast=True)

# RUN APP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
