var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');


socket.on('create room', function(msg){
    console.log(msg);
    $.ajax({
        url: msg['url']}).done(function(reply){
            $('#container').html(reply);
    });
});

document.querySelector("#join_room").addEventListener("click", () =>{
    console.log('poopoo');
    //TODO: check if fields are empty yadda yadda
    room_name = document.getElementById("room_input").value;
    user_name = document.getElementById("username_input").value;
    socket.emit("create room", {'room': room_name, 'user_name':user_name});
});