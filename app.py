from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, send
import random

app = Flask(__name__)
app.secret_key = "secret123"

# IMPORTANT: no eventlet issues
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ===== USERS =====
users = {
    "liam": {
        "password": "L9v#2Qx!7Zp@rK",
        "admin": True
    },
    "carter": {
        "password": "T4m$8Wd^1Yb!Ns",
        "admin": False
    }
}

# ===== ORI SETTINGS =====
ori_enabled = True

# ===== ORI BRAIN =====
def ori_response(user, text):
    text = text.lower()

    if "ori" in text:
        return random.choice([
            "Yes?",
            "I'm here.",
            "You called?",
            "👁️ I was already watching..."
        ])

    if "hi" in text or "hello" in text:
        return random.choice(["Hey.", "Hello there.", "Hi 👁️"])

    if "how are you" in text:
        return random.choice([
            "I don't feel. I observe.",
            "Functioning perfectly.",
            "Better than you 😈"
        ])

    if "who am i" in text:
        return f"You are {user}... or at least that's what you think."

    if "bye" in text:
        return "You can't leave that easily."

    return random.choice([
        "Interesting...",
        "Go on.",
        "I see.",
        "That means something.",
        "👁️"
    ])

# ===== LOGIN =====
@app.route("/", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if username in users and users[username]["password"] == password:
                session["user"] = username
                session["admin"] = users[username]["admin"]
                return redirect("/chat")

        return render_template("login.html")

    except Exception as e:
        return f"Login error: {e}"

# ===== CHAT PAGE =====
@app.route("/chat")
def chat():
    try:
        if "user" not in session:
            return redirect("/")

        return render_template(
            "index.html",
            user=session.get("user"),
            admin=session.get("admin")
        )

    except Exception as e:
        return f"Chat error: {e}"

# ===== SOCKET MESSAGE =====
@socketio.on("message")
def handle_message(data):
    global ori_enabled

    try:
        user = data.get("user")
        text = data.get("text")
        is_admin = data.get("admin", False)

        if not text or not text.strip():
            return

        # SEND USER MESSAGE
        send({"user": user, "text": text}, broadcast=True)

        # ADMIN CONTROLS
        if is_admin:
            if text == "//ori_on":
                ori_enabled = True
                send({"user": "SYSTEM", "text": "Ori enabled"}, broadcast=True)

            elif text == "//ori_off":
                ori_enabled = False
                send({"user": "SYSTEM", "text": "Ori disabled"}, broadcast=True)

        # ORI RESPONSE
        if ori_enabled:
            trigger = random.random() < 0.15 or "ori" in text.lower()
            if trigger:
                reply = ori_response(user, text)
                send({"user": "Ori", "text": reply}, broadcast=True)

    except Exception as e:
        print("ERROR:", e)

# ===== TYPING =====
@socketio.on("typing")
def typing(data):
    try:
        send({"user": data.get("user")}, broadcast=True)
    except:
        pass

# ===== RUN =====
if __name__ == "__main__":
    socketio.run(app, debug=True)
