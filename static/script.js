const socket = io();

const user = USER;
const isAdmin = ADMIN;

const chat = document.getElementById("chat");
const typingBox = document.getElementById("typing");

// ===== MESSAGE DISPLAY =====
socket.on("message", (data) => {
    let div = document.createElement("div");
    div.classList.add("msg");

    if (data.user === user) div.classList.add("me");
    else if (data.user === "Ori") div.classList.add("ori");
    else div.classList.add("other");

    div.innerHTML = `<b>${data.user}</b><br>${data.text}`;

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
});

// ===== TYPING =====
function typing(){
    socket.emit("typing", {user:user});
}

socket.on("typing", (data)=>{
    typingBox.innerText = data.user + " is typing...";
    setTimeout(()=>typingBox.innerText="",1000);
});

// ===== SEND MESSAGE =====
function sendMsg(){
    let msg = document.getElementById("msg");

    socket.emit("message", {
        user: user,
        text: msg.value,
        admin: isAdmin   // 🔥 THIS FIXES EVERYTHING
    });

    msg.value = "";
}

// ===== ADMIN HELPER =====
function sendAdmin(cmd){
    socket.emit("message", {
        user: user,
        text: cmd,
        admin: isAdmin
    });
}

// ===== BUTTON FUNCTIONS (ALL FIXED) =====
function ori(x){
    sendAdmin(x ? "//ori_on" : "//ori_off");
}

function toggleMorse(x){
    sendAdmin(x ? "//morse_on" : "//morse_off");
}

function setMorse(){
    let v = document.getElementById("morseSlider").value;
    sendAdmin("//morse_level " + v);
}

function oriSay(){
    let v = document.getElementById("oriText").value;
    sendAdmin("//ori_say " + v);
}

function oriMorse(){
    let v = document.getElementById("oriText").value;
    sendAdmin("//ori_morse " + v);
}
