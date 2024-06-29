$(document).ready(function() {
  var socket = io.connect('https://9c390d0a-dbf1-4996-92d8-bc663f3abf4d-00-352k79aiasl2l.picard.replit.dev/');

  socket.on("connect", function() {
    socket.send("a user connected.");
  });

  socket.on("message", message=>{
    let container = document.getElementById("message-container");
    console.log(container);
    container.innerHTML += `<p>${message}</p>`
  });

  function send_message(message, username) {
    socket.send(`${username}: ${message}`);
  }

  $("#send-btn").click(()=>{
    let username = document.getElementById("username-input").value;
    if (username == "") {
      username = "anonymous";
    }

    let message_to_send = document.getElementById("message-input").value;

    send_message(message_to_send, username);
    console.log(socket);
    // alert("click");
  });
});