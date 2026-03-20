const socket = io();

let user = prompt("Enter your name (Liam or Carter)");

function send() {
    let input = document.getElementById("msg");
    let text = input.value;

    socket.emit("message", {user: user, text: text});
    input.value = "";
}

// CARTER ONLY GAME PANEL
if (user === "Carter") {
    const gameContainer = document.createElement("div");
    gameContainer.innerHTML = `
        <button onclick="socket.emit('message',{user:'Carter',text:'//game TicTacToe'})">TicTacToe</button>
        <button onclick="socket.emit('message',{user:'Carter',text:'//game Trivia'})">Trivia</button>
        <button onclick="socket.emit('message',{user:'Carter',text:'//game MemoryMatch'})">Memory Match</button>
    `;
    document.body.appendChild(gameContainer);
}

socket.on("message", (data) => {
    let chat = document.getElementById("chat");
    let msg = document.createElement("div");
    msg.innerHTML = `<b>${data.user}:</b> ${data.text}`;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;

    if (data.glitch) {
        document.body.classList.add("glitch");
        setTimeout(()=>{document.body.classList.remove("glitch")},500);
    }
});

// ADMIN PANEL
socket.on("admin", (data) => {
    let panel = document.createElement("div");
    panel.style.position = "fixed";
    panel.style.bottom = "20px";
    panel.style.right = "20px";
    panel.style.background = "black";
    panel.style.color = "lime";
    panel.style.padding = "10px";
    panel.style.border = "1px solid lime";
    panel.innerHTML = "<b>ADMIN PANEL</b><br>" + data.commands.join("<br>");
    document.body.appendChild(panel);
});
