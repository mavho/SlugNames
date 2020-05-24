/*
Not sure what to name this page. Regardless this file should handle any elements, really the DOM of the
game UI

It also will obtain info and send info to the webservice
*/

var board_len = 5;
var board_width = 5;

console.log(user_name + ' ' + team + ' ' + role);
console.log(roomid);
/// load onclick handlers
$(document).ready(function() {
    console.log("Game page!");
    var thewords = $(".test");
    for(let r=0; r < board_len; r++){
        for(let c= 0; c<board_width; c++){
            thewords[(r*board_len)+c].addEventListener("click", bindClick(r,c));
        }
    }
 
    function bindClick(row, col) {
        return function() {
            console.log("row" + row + " :column " + col);
            socket.emit("flip card", {'row': row, 'col':col, 'roomid': roomid, 'username':user_name});
        };
    }
    /*
    On click handlers for sending stuff. For debugging
    */
    $("#send_clue_btn").click(function(){
        var clue = $("#clue_input").val();
        var amt = $("#card_amt_input").val();

        if(checkInput(clue,amt)){
            attemptSpyEmit(clue,amt);
        }else{
            alert("input is invalid");
        }
    });

    //TODO: do cell selection
    $("#send_cells_btn").click(function(){
        console.log("hello?")
        socket.emit("spy turn", {'roomid':roomid, 'turn':team});
        agent_turn = false;
    });



    /**
     * Hides clue container if not the spy master
     */
    if(!isSpyMaster()){
        $("#clue_cont").hide();
    }

    if(!isAgent()){
        $("#send_cell_cont").hide();
    }
});

var spy_turn = false;
var agent_turn = false;

socket.on('spy turn', function(msg){
    console.log("spymaster handler");
    console.log(msg);
    console.log(msg['turn'] + ' ' + team);
    if(role == "spymaster" && team == msg['turn']){
        console.log("It is " + msg['turn'] + " spymaster turn")
        spy_turn = true;
    }
    $("#debug").html(user_name + ' ' + team + ' ' + role
     + ' ' + turn + ' spyturn:' + spy_turn + ' agent turn:' + agent_turn + ' ' + clue_word);
});

//This signals the start of agent turn
socket.on('agent turn', function(msg){
    console.log("agent handler");
    console.log(msg);
    cardQ_len = msg['amt']
    clue_word = msg['clue']

    if(team == msg['turn'] && role=="agent"){
        console.log("agent turn");
        agent_turn = true;
    }
    $("#debug").html(user_name + ' ' + team + ' ' + role
     + ' ' + turn + ' spyturn:' + spy_turn + ' agent turn:' + agent_turn + ' ' + clue_word);
});

// This needs to handle receiving  a card event from someone.
socket.on('flip card', function(msg){
    console.log(msg);
});

// Wrapper for emit, check if you have permissions to emit.
function attemptSpyEmit(clue,amt){
    if (spy_turn){
        socket.emit("agent turn",{'clue':clue,'amt':amt,'roomid':roomid});
        spy_turn = false;
    }
}

function isSpyMaster(){
    return role == "spymaster";
}
function isAgent(){
    return role == "agent";
}

function checkInput(clue, amt){
    if(clue == '' || isNaN(amt) || amt == ''){
        return false;
    }
    return true
}