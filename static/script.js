const socket = io();

const user = USER;
const isAdmin = ADMIN;

const chat = document.getElementById("chat");

// TIME
function getTime(){
    let d = new Date();
    return d.getHours() + ":" + String(d.getMinutes()).padStart(2,'0');
}

// AVATAR LETTER
function avatarLetter(name){
    return name.charAt(0).toUpperCase();
}

// MESSAGE DISPLAY
socket.on("message", (data) => {

    let row = document.createElement("div");
    row.classList.add("msg");

    if (data.user === user) row.classList.add("me");
    else if (data.user === "Ori") row.classList.add("ori");
    else row.classList.add("other");

    // avatar
    let avatar = document.createElement("div");
    avatar.classList.add("avatar");
    avatar.innerText = avatarLetter(data.user);

    // bubble
    let bubble = document.createElement("div");
    bubble.classList.add("bubble");

    bubble.innerHTML = `
        <b>${data.user}</b><br>
        ${data.text}
        <div class="time">${getTime()}</div>
    `;

    // layout
    if (data.user === user){
        row.appendChild(bubble);
    } else {
        row.appendChild(avatar);
        row.appendChild(bubble);
    }

    chat.appendChild(row);
    chat.scrollTop = chat.scrollHeight;
});

// SEND
function sendMsg(){
    let msg = document.getElementById("msg");

    socket.emit("message", {
        user: user,
        text: msg.value,
        admin: isAdmin
    });

    msg.value="";
}

// ENTER KEY
document.getElementById("msg").addEventListener("keypress", function(e){
    if(e.key === "Enter") sendMsg();
});

// ADMIN
function toggleAdmin(){
    let p = document.getElementById("adminPanel");
    p.style.right = p.style.right === "0px" ? "-260px" : "0px";
}

function sendAdmin(cmd){
    socket.emit("message", {
        user: user,
        text: cmd,
        admin: isAdmin
    });
}

function ori(x){
    sendAdmin(x ? "//ori_on" : "//ori_off");
}
