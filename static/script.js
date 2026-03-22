const socket = io();
let user = prompt("Name:");

const chat = document.getElementById("chat");
const typingBox = document.getElementById("typing");

// MESSAGES
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

// TYPING
function typing(){
    socket.emit("typing", {user:user});
}

socket.on("typing", (data)=>{
    typingBox.innerText = data.user + " is typing...";
    setTimeout(()=>typingBox.innerText="",1000);
});

// SEND
function sendMsg(){
    let msg = document.getElementById("msg");
    socket.emit("message",{user:user,text:msg.value});
    msg.value="";
}

// ADMIN
function toggleAdmin(){
    let p = document.getElementById("adminPanel");
    p.style.right = p.style.right === "0px" ? "-250px" : "0px";
}

function ori(x){
    socket.emit("message",{user:user,text:x?"//ori_on":"//ori_off"});
}
