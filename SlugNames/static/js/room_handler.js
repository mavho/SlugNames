var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

socket.on('create room', function(msg){
    $("#join_room").hide();
    $("#create_room").hide();
    console.log(msg);
    allusers = msg['allusers'];
    $("#users_list").empty(); //just clear the list each time so we don't have duplicates
    for (var i = 0; i < allusers.length; i++) {
        console.log("User " + i + "found.");
        console.log(allusers[i]);
        var aUser = $('<li class="list-group-item"/>');
        aUser.innerHTML = allusers[i];
        $("#users_list").append(allusers[i]); //show all users on the page 
        $("#users_list").append("<br>");
    }
    var startButton = $('<button/>').text('Start the game').click(function () { 
        socket.emit("start game", {'room': msg['room'], 'hardStart': 'false'});
    });

    var startButton2 = $('<button/>').text('HARD START').click(function () { 
        socket.emit("start game", {'room': msg['room'], 'hardStart': 'true'});
    });
    $("#start_shit").append(startButton); 
    $("#start_shit").append(startButton2); //startButton2 just makes it so you dont need 4 players, for debugging
    // $("#users_list").append({"class": "list-group-item", "innerHTML" : "a user"});
});

socket.on('join theroom', function(msg){
    $("#join_room").hide();
    $("#create_room").hide();
    console.log(msg);
    allusers = msg['allusers'];
    $("#users_list").empty();
    for (var i = 0; i < allusers.length; i++) {
        console.log("User " + i + "found.");
        console.log(allusers[i]);
        var aUser = $('<li class="list-group-item"/>');
        aUser.innerHTML = allusers[i];
        $("#users_list").append(allusers[i]); //show all users on the page 
        $("#users_list").append("<br>");
    }
});

socket.on('start game', function(msg) {
    $.ajax({
        url: msg['url']}).done(function(reply){
            $('#container').html(reply);
    });
})

document.querySelector("#create_room").addEventListener("click", () =>{
    console.log('create room');
    //TODO: check if fields are empty yadda yadda
    room_name = document.getElementById("room_input").value;
    user_name = document.getElementById("username_input").value;
    socket.emit("create room", {'room': room_name, 'user_name':user_name});
});

document.querySelector("#join_room").addEventListener("click", () => {
    console.log("join room");
    room_name = document.getElementById("room_input").value;
    user_name = document.getElementById("username_input").value;
    socket.emit("join theroom", {'room': room_name, 'user_name':user_name});

})