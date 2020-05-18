/*
Not sure what to name this page. Regardless this file should handle any elements, really the DOM of the
game UI

It also will obtain info and send info to the webservice
*/

$(document).ready(function() {
    console.log("Game page!");
    var thewords = $(".test");
    for(var i = 0; i < thewords.length; i++) {
        thewords[i].addEventListener("click", bindClick(i));
    }
 
    function bindClick(i) {
        return function() {
            console.log("this number was clicked:  " + i);
            socket.emit("flip card", {'card': i,  'roomid': roomid });
        };
    }
});