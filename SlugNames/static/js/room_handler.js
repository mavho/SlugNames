var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
/**
 * These vars are not meant to be altered, treat them as static
 */
var user_name = "";
var team = "";
var role = "";
/**
 * These vars are meant to be altered
 */
var cardQ = {};
var cardQ_len = 0;;
var clue_word = "";
var flipped_cards = {};

/**
 * Turn can only be one of two values. R or B
 */
var turn = "";


/**
 * Called upon creating a room
 */
socket.on('create room', function(msg){
    hideButtons();
    // console.log(msg);
    allusers = msg['allusers'];
    createUsersList(allusers);
    var startButton = $('<button type="button" class="btn btn-primary"/>').text('Start the game');
    // startButton.classList.add('btn-primary');
    startButton.click(function () { 
        socket.emit("start game", {'room': msg['room'], 'hardStart': 'false'});
    });

    var hardStart = $('<button type="button" class="btn btn-primary"/>').text('HARD START'); 
    hardStart.click(function () { 
        socket.emit("start game", {'room': msg['room'], 'hardStart': 'true'});
    });
    $("#start_btnsection").append(startButton); 
    $("#start_btnsection").append("</br> <br>");
    $("#start_btnsection").append(hardStart); //startButton2 just makes it so you dont need 4 players, for debugging
    // $("#users_list").append({"class": "list-group-item", "innerHTML" : "a user"});
});

/**
 * Called upon joining a room
 */
socket.on('join theroom', function(msg){
    hideButtons();
    console.log('Join theroom ' + msg);
    allusers = msg['allusers'];
    createUsersList(allusers);
});

function createUsersList(allusers){
    $("#users_list").empty();
    var aheading= $('<h3/>').text("Players:");
    $("#users_list").append(aheading);
    for (var i = 0; i < allusers.length; i++) {
        // console.log("User " + i + "found.");
        // console.log(allusers[i]);
        // var aUser = $('<li class="list-group-item"/>').text(allusers[i]);
        if(allusers[i] == user_name){
            var aUser = $('<li class="list-group-item list-group-item-info"/>').text(allusers[i]);
        }
        else{
            var aUser = $('<li class="list-group-item"/>').text(allusers[i]);
        }
        // aUser.innerHTML = allusers[i];
        $("#users_list").append(aUser);
        $("#users_list").append("<br>");
    }
}

function hideButtons(){
    $("#join_room").hide();
    $("#create_room").hide();
    $("#startButtons").hide();
}

/**
 * This is called upon the room creator starting the game. Roles are defined.
 */
socket.on('start game', function(msg) {
    var theurl = msg['url'];
    console.log('Start the game');
    if (msg['spy'] == true){
        console.log('You are a spymaster on team ' + msg['team']);
        role = "spymaster";
        team = msg['team']
        theurl = '/spygame/' + room_name;
        if (team == 'blue'){
            isBlueSpyMaster = true;
        }
    }
    else{
        console.log('You are a agent on team ' + msg['team']);
        role = "agent";
        team = msg['team']
    }
    let turn = "start";
    $.ajax({
        url: theurl, 
        // url: theurl, 
        }).done(function(reply){
            $('#container').html(reply);
            console.log("emitting start of game" + turn);
            //This essentially starts the game!
            socket.emit("spy turn", {'turn':turn, 'roomid':roomid});
            $('#maintitle').append("Player: " + user_name);
            $('#maintitle').append(" Team: " + team);
            $('#maintitle').append(" Role: " + role);
    });
});

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
});