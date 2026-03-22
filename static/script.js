const socket = io();
let user = prompt("Name?");

const chat = document.getElementById("chat");

socket.on("message", (data) => {
    let div = document.createElement("div");
    div.innerText = data.user + ": " + data.text;
    chat.appendChild(div);
});

function sendMsg() {
    let text = document.getElementById("msg").value;
    socket.emit("message", {user:user, text:text});
}


// ===== ADMIN PANEL =====
if (user === "Liam") {
    document.getElementById("adminPanel").style.display = "block";
} else {
    document.getElementById("adminPanel").style.display = "none";
}

// controls
function toggleOri(x){ socket.emit("message",{user,text:x?"//ori_on":"//ori_off"}) }
function toggleMorse(x){ socket.emit("message",{user,text:x?"//morse_on":"//morse_off"}) }
function setMorse(){
    let v=document.getElementById("morseSlider").value;
    socket.emit("message",{user,text:"//morse_level "+v})
}
function oriSay(){
    let v=document.getElementById("oriText").value;
    socket.emit("message",{user,text:"//ori_say "+v})
}
function oriMorse(){
    let v=document.getElementById("oriText").value;
    socket.emit("message",{user,text:"//ori_morse "+v})
}
function alertSys(){ socket.emit("message",{user,text:"//ori_alert"}) }
function glitch(){ socket.emit("message",{user,text:"//ori_glitch"}) }


// ===== CARTER GAMES =====
if (user === "Carter") {
    document.getElementById("games").innerHTML = `
        <h3>🎮 Games</h3>
        <button onclick="openGame('snake')">Snake</button>
        <button onclick="openGame('tetris')">Tetris</button>
        <button onclick="openGame('pacman')">Pacman</button>
    `;
}

function openGame(g){
    if(g==="snake") window.open("https://playsnake.org/");
    if(g==="tetris") window.open("https://tetris.com/play-tetris");
    if(g==="pacman") window.open("https://playsnake.org/pacman");
}
