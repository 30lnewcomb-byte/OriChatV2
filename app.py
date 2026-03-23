from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = "secret123"
socketio = SocketIO(app)

# USERS
users = {
    "liam": {"password": "L9v#2Qx!7Zp@rK", "admin": True},
    "carter": {"password": "T4m$8Wd^1Yb!Ns", "admin": False}
}

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")

        if u in users and users[u]["password"] == p:
            session["user"] = u
            session["admin"] = users[u]["admin"]
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

# CARTER GAME PAGE
@app.route("/carter-game")
def carter_game():
    if "user" not in session:
        return redirect("/")

    if session["user"] != "carter":
        return "Access denied"

    return render_template("games.html")

# RUN
if __name__ == "__main__":
    socketio.run(app, debug=True)
