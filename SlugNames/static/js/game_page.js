/*
Not sure what to name this page. Regardless this file should handle any elements, really the DOM of the
game UI

It also will obtain info and send info to the webservice
*/

var board_len = 5;
var board_width = 5;
console.log(user_name + ' ' + team + ' ' + role + ' ' + roomid);
/// load onclick handlers
$(document).ready(function() {
    console.log("Game page!");
    var thewords = $(".test");
    for(let r=0; r < board_len; r++){
        for(let c= 0; c<board_width; c++){
            thewords[(r*board_len)+c].addEventListener("click", bindClick(r,c));
            //attach a specific id to each button 
            thewords[(r*board_len)+c].setAttribute("id", r + '-' + c);
        }
    }
    $("#debug").html(user_name + ' ' + team + ' ' + role
     + ' ' + turn + ' spyturn:' + spy_turn + ' agent turn:' + agent_turn);
    function bindClick(row, col) {
        return function() {
            if(role != 'spymaster' && agent_turn){
                let tostr = row + "" + col;
                let tab_rc = $("#" + row + '-'+col);

                //User is not able to select any card in already flipped cards
                if(tostr in flipped_cards){
                    return;
                }
                if(tostr in cardQ){
                    delete cardQ[tostr];
                    tab_rc.css('border-color','white');
                    tab_rc.css('background-color','white');
                }else if (Object.keys(cardQ).length < cardQ_len){
                    cardQ[tostr] = {'row':row,'col':col};
                    tab_rc.css('border-color','green');
                    tab_rc.css('background-color','green');
                }
            }
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
        attemptAgentEmit();
    });
    /**
     * Hides divs not needed by current role
     */
    if(!isSpyMaster()){
        $("#clue_cont").hide();
    }

    if(!isAgent()){
        $("#send_cell_cont").hide();
    }
});

/**
 * spy_turn is true if role is spymaster and cur team's turn
 * agent_turn is true if role is agent and cur team's turn
 */
var spy_turn = false;
var agent_turn = false;

//Signals start of spy turn
socket.on('spy turn', function(msg){

    console.log(msg);
    //TODO: cleanup end screen etc.
    if(msg['end'] == true){
        $("#debug").html('GAME OVER ' + msg['turn'] + ' Loses');
        return;
    }
    updateCardColors(msg['flippedCards']);

    if(role == "spymaster" && team == msg['turn']){
        console.log("It is " + msg['turn'] + " spymaster turn");
        spy_turn = true;
    }
    $("#debug").html(user_name + ' ' + team + ' ' + role
     + ' ' + turn + ' spyturn:' + spy_turn + ' agent turn:' + agent_turn + ' ' + clue_word);
});

//This signals the start of agent turn
socket.on('agent turn', function(msg){
    cardQ_len = msg['amt']
    clue_word = msg['clue']
    if(team == msg['turn'] && role=="agent"){
        console.log("It is " + msg['turn'] + " agent's turn");
        agent_turn = true;
    }
    $("#debug").html(user_name + ' ' + team + ' ' + role
     + ' ' + turn + ' spyturn:' + spy_turn + ' agent turn:' + agent_turn + ' ' + clue_word);
});

// This needs to handle receiving  a card event from someone.
// TODO: error checking or something
socket.on('flip card', function(msg){
    console.log(msg);
});


function updateCardColors(cards) {
    //updates UI for all cards
    for (let key in cards) {
        let number = parseInt(key);
        let row = Math.floor(number / 10);
        row = row.toString();
        let col = number % 10;
        col = col.toString();
        let tostr = row + "" + col;

        let tab_rc = $("#" + row + '-' + col);
        if (cards[tostr] == 'R') {
            tab_rc.css('border-color', 'red');
            flipped_cards[tostr] ='R';
        }
        else if (cards[tostr] == 'B') {
            tab_rc.css('border-color', 'blue');
            flipped_cards[tostr] ='B';
        }
        else if (cards[tostr] == 'I') {
            tab_rc.css('border-color', 'white');
            flipped_cards[tostr] ='I';
        }
        else {
            tab_rc.css('border-color', 'black');
            flipped_cards[tostr] ='A';
            console.log('Brah i think you lost!');
        }
    }
}
// Wrapper for emit, check if you have permissions to emit.
// emits and ends spy turn
function attemptSpyEmit(clue,amt){
    if (spy_turn){
        socket.emit("agent turn",{'clue':clue,'amt':amt,'roomid':roomid});
        spy_turn = false;
    }
}

//We set agent turn to false once they send to prevent them from sending multiple, even thought the next phase hasn't started
function attemptAgentEmit(){
    console.log("ATTEMPTING EMIT");
    if(agent_turn){
        console.log("ATTEMPTING EMIT");
        socket.emit("flip card", {'roomid':roomid, 'turn':team, 'cards':cardQ});
        agent_turn = false;
        //remove styling from the cardQ, then reset it
        for(let card of Object.keys(cardQ)){
            let rc = cardQ[card];
            let tab_rc = $("#" + rc['row'] + '-'+ rc['col']);
            tab_rc.css('border-color','grey');
            tab_rc.css('background-color','white');
        }
        cardQ = {};
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
    return true;
}