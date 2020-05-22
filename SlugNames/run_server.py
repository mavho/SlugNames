from flask import Flask, render_template,url_for, request, jsonify, redirect
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit,join_room,leave_room
from RoomMaster import RoomMaster
from config import Config
import os,sys

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

### We'll use a dictionary to keep track of the games
### TODO: We'll want to either implement a DB or redis later. This will be fine for now
CHANNELS = {}


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('layouts/index.html')

@app.route('/game/<roomid>', methods=['GET'])
def theGame(roomid):
    # print(CHANNELS[roomid].word_board, file=sys.stderr)
    #thenames is a 5x5 2d list with the words for codenames 

    return render_template('layouts/game_room.html', thenames=CHANNELS[roomid].word_board, roomid=roomid)   #thenames=CHANNELS[roomid].word_board)



@socketio.on('create room',namespace='/test')
def create_room(data):
    """
    sends caller back a room master object and url
    Wait no room master obj isn't seriliazable, we need to return stuff from it
    The js files should build off that
    This can be used either to join a create a room.
    """
    GM = RoomMaster()
    room = data['room']
    user_name = data['user_name']
    ## TODO: Check for duplicate rooms. Return different templates
    CHANNELS[room] = GM 
    join_room(room)
    url = url_for('theGame', roomid=room) 
    print("Client " + user_name + " joined " + room, file=sys.stderr)
    emit('create room', {'GM': str(GM.word_board), 'url': url}, room=room)

@socketio.on('flip card', namespace='/test')
def flip_card(data):
    """
    An example url that handles some event. 
    TODO: Client side needs to access this somehow
    """
    # data should have room name or something
    print('Flip card ' + str(data['row']) + ' ' + str(data['col']) + ' ' +  str(data['roomid']) , file=sys.stderr)
    room = data['roomid']
    row = data['row']
    col = data['col']
    GM = CHANNELS[room]
    print(GM.word_board,file=sys.stderr)
    print(GM.state_board,file=sys.stderr)
    action = GM.flipCard(row,col)
    emit('flip card',{'row': row, 'col': col, 'action':action}, room=room, include_self=False)


@socketio.on('connect',namespace='/test')
def test_connect():
    print('Client connected',file=sys.stderr)
    emit('my response',{'data':'Hello'})

@socketio.on('disconnect',namespace='/test')
def test_disconnect():
    print('Client disconnected', file=sys.stderr)


if __name__ == '__main__':
    app.debug=True
    socketio.run(app,host='localhost')