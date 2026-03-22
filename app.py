from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.secret_key = "secret123"

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ===== DATABASE =====
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

# ===== GLOBAL =====
ori_enabled = True
current_prank = None
user_behavior = {}

# ===== ANALYZE =====
def analyze_message(text):
    text = text.lower()
    good = ["hi", "hello", "thanks", "please", "nice"]
    bad = ["hate", "idiot", "stupid", "shut up"]

    score = 0
    for w in good:
        if w in text:
            score += 1
    for w in bad:
        if w in text:
            score -= 2

    if score > 0: return "good"
    if score < 0: return "bad"
    return "neutral"

# ===== ORI =====
def ori_response(user, text):
    mood = analyze_message(text)
    rep = user_behavior.get(user, 0)

    if rep > 5:
        return random.choice(["You're easy to talk to.", "I like this convo.", "You're chill."])
    if rep < -5:
        return random.choice(["Let's keep it better.", "Not great.", "Try again."])

    if mood == "good":
        return random.choice(["Nice.", "Good energy.", "👍"])
    if mood == "bad":
        return random.choice(["Relax.", "Chill.", "Not needed."])

    if "game" in text.lower():
        return "Try the games button at the top."

    return random.choice(["Ok.", "Interesting.", "Alright."])

# ===== ROUTES =====
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username").lower().strip()
        password = request.form.get("password").strip()

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session["user"] = user.username
            session["admin"] = user.admin
            return redirect("/chat")
        else:
            error = "Invalid login"

    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").lower().strip()
        password = request.form.get("password").strip()

        if User.query.filter_by(username=username).first():
            return "User exists"

        new_user = User(username=username, password=password, admin=False)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/")

    return render_template("register.html")

@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html", user=session["user"], admin=session["admin"])

@app.route("/games")
def games():
    if "user" not in session:
        return redirect("/")
    return render_template("games.html")

# ===== SOCKET =====
@socketio.on("message")
def handle_message(data):
    global ori_enabled, current_prank

    user = data.get("user")
    text = data.get("text")
    is_admin = data.get("admin", False)

    if not text:
        return

    mood = analyze_message(text)

    if user not in user_behavior:
        user_behavior[user] = 0

    if mood == "good":
        user_behavior[user] += 1
    elif mood == "bad":
        user_behavior[user] -= 2

    if mood == "bad" and user_behavior[user] < -5:
        send({"user": "SYSTEM", "text": "⚠️ Blocked"}, broadcast=True)
        return

    send({"user": user, "text": text}, broadcast=True)

    # ADMIN
    if is_admin:
        if text == "//ori_on": ori_enabled = True
        elif text == "//ori_off": ori_enabled = False
        elif text.startswith("//prank "):
            current_prank = text.replace("//prank ", "")
            send({"user": "SYSTEM", "text": "Prank sent"}, broadcast=True)

    # ORI
    if ori_enabled and random.random() < 0.2:
        send({"user": "Ori", "text": ori_response(user, text)}, broadcast=True)

# ===== RUN =====
if __name__ == "__main__":
    socketio.run(app, debug=True)
