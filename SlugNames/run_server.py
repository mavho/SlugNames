from flask import Flask, render_template,url_for, request, jsonify, redirect
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit,join_room,leave_room
from RoomMaster import RoomMaster
from config import Config
import os,sys, random

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

### We'll use a dictionary to keep track of the games
### TODO: We'll want to either implement a DB or redis later. This will be fine for now
CHANNELS = {}

### tracks sid and associates with user,room
sid_username_room = {}

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('layouts/index.html')

@app.route('/game/<roomid>', methods=['GET'])
def theGame(roomid):
    return render_template('layouts/game_room.html', thenames=CHANNELS[roomid].word_board, roomid=roomid)   #thenames=CHANNELS[roomid].word_board)

#a really shitty way of doing it but idk
@app.route('/spygame/<roomid>', methods=['GET'])
def spyGame(roomid):
    return render_template('layouts/game_room.html', thenames=CHANNELS[roomid].word_board, boardstate=CHANNELS[roomid].state_board, roomid=roomid)   #thenames=CHANNELS[roomid].word_board)


#Host creates a room, and is able to start the game 
@socketio.on('create room',namespace='/test')
def create_room(data):
    """
    sends caller back a room master object and url
    """
    GM = RoomMaster()
    room = data['room']
    user_name = data['user_name']
    ## TODO: Check for duplicate rooms. Return different templates
    if(CHANNELS.get(room) is None):
        host = True 
        CHANNELS[room] = GM
    else: 
        print("Duplicate room!", file=sys.stderr)
        return
    join_room(room)
    url = url_for('theGame', roomid=room) 
    GM.users.append(user_name)
    GM.usersid[user_name] = request.sid 
    sid_username_room[request.sid] = (user_name,room)
    print("Host " + user_name + " created " + room, file=sys.stderr)  

    emit('create room', {'GM': str(GM.word_board), 'url': url, 'user': str(user_name), 'allusers': GM.users, 'room': room}, room=room)

#users join room that a host created 
#this is a lot of duplicate code, can probably refactor later 
@socketio.on('join theroom', namespace='/test')
def join_theroom(data):
    room = data['room']
    user_name = data['user_name']
    if(CHANNELS.get(room) is None):
        print("Room doesn't exist you bumbo", file=sys.stderr)
        return
    GM = CHANNELS[room]
    if(user_name in GM.users):
        print("Duplicate username", file=sys.stderr)
        return 
    join_room(room)
    url = url_for('theGame', roomid=room)
    print("Client " + user_name +" joined " + room, file=sys.stderr)
    GM.users.append(user_name)
    GM.usersid[user_name] = request.sid
    sid_username_room[request.sid] = (user_name,room)
    emit('join theroom', {'GM': str(GM.word_board), 'url': url, 'user': str(user_name), 'allusers': GM.users}, room=room)

@socketio.on('start game', namespace='/test')
def start_game(data):
    room = data['room']
    if(CHANNELS.get(room) is None):
        print("Tried to start game but room doesn't exist... strange", file=sys.stderr)
        return
    GM = CHANNELS[room]
    if( (len(GM.users) < 4) and (data['hardStart'] == 'false') ):
        print("Need at least 4 users", file=sys.stderr)
        return
        
    #putting the users into teams 
    for index, user in enumerate(GM.users): 
        if(index % 2) == 0:
            GM.team_red.append(user)
        else:
            GM.team_blue.append(user)
    #selecting spymaster amongst the teams
    spyred = random.randrange(0, len(GM.team_red))
    spyblue = random.randrange(0, len(GM.team_blue))
    GM.spymasters.append(GM.team_red[spyred])
    GM.spymasters.append(GM.team_blue[spyblue])
    url = url_for('theGame', roomid=room)
    for user in GM.team_red:
        is_spy = False
        if user in GM.spymasters:
            is_spy = True
        emit('start game', {'url': url, 'spy': is_spy, 'team': 'red', 'turn': GM.current_turn}, room=GM.usersid[user])
    for user in GM.team_blue:
        is_spy = False
        if user in GM.spymasters: 
            is_spy = True
        emit('start game', {'url': url, 'spy' : is_spy, 'team': 'blue', 'turn': GM.current_turn}, room=GM.usersid[user])


### the spy turn has started.
@socketio.on('spy turn',namespace='/test')
def spy_phase(data):
    """
    Action handler. We have to evaluate the cells they send us.
    given special turn start, turn will be blue. Only invoked at start
    """
    room = data['roomid']
    turn = data['turn']
    GM = CHANNELS.get(room)
    if GM is None:
        print("Handle error")
    if turn == "start":
        emit('spy turn', {'turn': 'blue'}, room=room,include_self=True)
    else:
        emit('spy turn', {'turn':GM.current_turn}, room=room, include_self=True)

### signals start of agent turn, broadcast it
@socketio.on('agent turn',namespace='/test')
def agent_turn(data):
    print('Agent turn broadcast',file=sys.stderr)
    room=data['roomid']
    clue = data['clue']
    amt = data['amt']

    GM = CHANNELS.get(room)
    GM.clue_amt = amt
    if GM is None:
        print("Handle error")

    emit('agent turn', {'turn': GM.current_turn, 'clue':clue, 'amt':amt}, room=room)


@socketio.on('flip card', namespace='/test')
def flip_card(data):
    """
    Agents send their cardQ to this route.
    Once all agents have sent their cardQ,
    the server will emit out spy turn, signalling
    start of the next spy turn

    TODO: timer implementation
    """
    room = data['roomid']
    cur_turn = data['turn']
    cards = data['cards']
    GM = CHANNELS[room]
    GM.senders += 1
    ### if not all senders have sent their cards dont continue
    if GM.maxSenders(cards,cur_turn) != 'OK':
        return

    print('Send emit to spy turn', file=sys.stderr)
    
    ACTION = GM.determineAction(cards,cur_turn)

    new_turn = cur_turn # var to store the turn
    end = False # flag to end the game
    win = {'state':False,'team':''} 

    if ACTION == 'ASSASSIN':
        end=True
    elif ACTION == 'SWITCH':
        new_turn = 'blue' if cur_turn =='red' else 'red'
    elif ACTION == 'BLUE':
        win['state'] = True
        win['team'] = 'blue'
    elif ACTION=='RED':
        win['state'] = True
        win['team'] = 'red'

    GM.current_turn = new_turn
    # reset agent turn vars 
    GM.senders = 0
    GM.cardQ = {}
    emit('spy turn',{'turn':new_turn,'roomid':room, 'flippedCards':GM.flippedCards, 'end':end,'win':win}, room=room)


@socketio.on('connect',namespace='/test')
def test_connect():
    print('Client connected ' + request.sid, file=sys.stderr)
    emit('my response',{'data':'Hello'})

@socketio.on('disconnect',namespace='/test')
def test_disconnect():
    print('This guy disconnected: ' + request.sid, file=sys.stderr)
    if request.sid in sid_username_room:
        user,room= sid_username_room[request.sid]
        GM = CHANNELS[room]
        #(user,room)
        leave_room(room)
        del sid_username_room[request.sid]
        GM.removeUser(user)
        emit('disconnect', {'user': user}, room=room)


if __name__ == '__main__':
    app.debug=True
    socketio.run(app,host='localhost')