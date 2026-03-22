const socket = io();
let user = prompt("Enter your name:");

const chat = document.getElementById("chat");

// MESSAGE RENDER
socket.on("message", (data) => {
    let div = document.createElement("div");
    div.classList.add("message");

    if (data.user === user) {
        div.classList.add("me");
    } else if (data.user === "Ori") {
        div.classList.add("ori");
    } else {
        div.classList.add("other");
    }

    div.innerText = data.user + ": " + data.text;

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
});

// SEND
function sendMsg() {
    let text = document.getElementById("msg").value;
    socket.emit("message", {user:user, text:text});
    document.getElementById("msg").value = "";
}

// ADMIN PANEL
if (user === "Liam") {
    document.getElementById("adminPanel").style.display = "block";
} else {
    document.getElementById("adminPanel").style.display = "none";
}

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
