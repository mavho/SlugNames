/*
Not sure what to name this page. Regardless this file should handle any elements, really the DOM of the
game UI

It also will obtain info and send info to the webservice
*/

var board_len = 5;
var board_width = 5;
console.log(user_name + ' ' + team + ' ' + role);
console.log(roomid);
$(document).ready(function() {
    console.log("Game page!");
    var thewords = $(".test");
    for(let r=0; r < board_len; r++){
        for(let c= 0; c<board_width; c++){
            thewords[(r*board_len)+c].addEventListener("click", bindClick(r,c));
            thewords[(r*board_len)+c].setAttribute("id", r + '-' + c);
        }
    }
 
    function bindClick(row, col) {
        return function() {
            if(role != 'spymaster'){
                console.log("row" + row + " :column " + col);
                socket.emit("flip card", {'row': row, 'col':col, 'roomid': roomid, 'username':user_name});
                $('#' + row + '-' + c).append('clicked');
            }
        };
    }
});


// This needs to handle receiving  a card event from someone.
socket.on('flip card', function(msg){
    console.log(msg);
});