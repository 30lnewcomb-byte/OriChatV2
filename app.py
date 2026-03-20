from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import random, time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# ----------------- STATE -----------------
messages = []
ori_memory = []
admins = ["Liam"]

user_profiles = {
    "Liam": {"admin": True, "games": []},
    "Carter": {"admin": False, "games": ["TicTacToe", "Trivia", "MemoryMatch"]}
}

prank_commands = ["//fake","//invis","//scramble","//reverse","//glitch","//ghost"]

last_hint_time = 0
hint_index = 0

# ----------------- HELPERS -----------------
def is_admin(user):
    return user in admins

def remember(user, text):
    ori_memory.append({"user": user, "text": text})
    if len(ori_memory) > 50:
        ori_memory.pop(0)

def scramble(text):
    return ''.join(random.sample(text, len(text)))

def get_next_hint():
    global hint_index
    if hint_index < len(prank_commands):
        hint = prank_commands[hint_index]
        hint_index += 1
        return hint
    return None

def maybe_drop_hint(user):
    global last_hint_time
    if is_admin(user) or user != "Carter":
        return

    now = time.time()
    if now - last_hint_time > random.randint(60, 120):
        hint = get_next_hint()
        if hint:
            last_hint_time = now
            messages.append({
                "user": "Ori",
                "text": random.choice([
                    f"...strange pattern detected: {hint[:2]}???",
                    f"I saw something like '{hint[0]}{hint[1]}...' earlier...",
                    f"⚠️ fragment: {hint[:3]}???",
                    f"memory glitch → {hint[0]} _ _"
                ])
            })

def memory_react():
    for m in ori_memory:
        if "secret" in m["text"].lower():
            return "👁️ I remember someone mentioned a secret..."
    return None

def is_game_message(user, text):
    return text.startswith("//game")

def handle_game(user, text):
    command = text.replace("//game ","")
    if command in user_profiles[user]["games"]:
        send({"user":"System","text":f"🎮 {command} started for {user}!"}, broadcast=True)
    else:
        send({"user":"System","text":"❌ Unknown game."}, broadcast=True)

# ----------------- ROUTES -----------------
@app.route('/')
def index():
    return render_template('index.html')

# ----------------- SOCKET -----------------
@socketio.on('message')
def handle_message(data):
    global messages

    user = data.get("user")
    text = data.get("text")

    # ----------------- GAME CHECK -----------------
    if is_game_message(user, text):
        handle_game(user, text)
        return  # Ori ignores game messages completely

    remember(user, text)

    # ----------------- ADMIN PANEL -----------------
    if is_admin(user) and text == "//admin":
        emit("admin", {
            "commands": prank_commands
        })
        return

    # ----------------- PRANKS -----------------
    if "//fake" in text:
        msg = text.replace("//fake","")
        messages.append({"user":"Carter","text":msg})
        send({"user":"Carter","text":msg}, broadcast=True)
        return

    if "//invis" in text:
        msg = text.replace("//invis","")
        html = f"<span style='opacity:0'>{msg}</span>"
        messages.append({"user":user,"text":html})
        send({"user":user,"text":html}, broadcast=True)
        return

    if "//scramble" in text:
        msg = scramble(text.replace("//scramble",""))
        messages.append({"user":user,"text":msg})
        send({"user":user,"text":msg}, broadcast=True)
        return

    if "//reverse" in text:
        msg = text.replace("//reverse","")[::-1]
        messages.append({"user":user,"text":msg})
        send({"user":user,"text":msg}, broadcast=True)
        return

    if "//ghost" in text:
        msg = text.replace("//ghost","")
        messages.append({"user":user,"text":msg})
        send({"user":user,"text":msg}, broadcast=True)

        def remove():
            time.sleep(2)
            if messages:
                messages.pop()
                send({"user":"Ori","text":"(a message vanished...)"}, broadcast=True)

        socketio.start_background_task(remove)
        return

    if "//glitch" in text:
        send({"user":"System","text":"⚠️ GLITCH TRIGGERED","glitch":True}, broadcast=True)
        return

    # ----------------- NORMAL MESSAGE -----------------
    msg = {"user":user,"text":text}
    messages.append(msg)
    send(msg, broadcast=True)

    # ----------------- SYSTEM ALERTS -----------------
    if random.random() < 0.1:
        alert = random.choice([
            "⚠️ Network instability detected",
            "🔐 Unauthorized access attempt",
            "📡 Signal interference detected",
            "💾 Memory scan running..."
        ])
        send({"user":"System","text":alert}, broadcast=True)

    # ----------------- MEMORY REACTION -----------------
    if random.random() < 0.2:
        mem = memory_react()
        if mem:
            send({"user":"Ori","text":mem}, broadcast=True)

    # ----------------- HINT SYSTEM -----------------
    maybe_drop_hint(user)

# ----------------- RUN -----------------
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
