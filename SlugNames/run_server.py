from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, emit
from RoomMaster import RoomMaster
from config import Config
import os,sys

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('layouts/index.html')

@app.route('/game', methods=['GET'])
def theGame():
    GM = RoomMaster()
    #thenames is a 5x5 2d list with the words for codenames 
    return render_template('layouts/game_room.html')

@socketio.on('connect',namespace='test')
def test_connect():
    print('Client connected',file=sys.stderr)
    emit('my response',{'data':'Hello'})

@socketio.on('disconnect',namespace='test')
def test_disconnect():
    print('Client disconnected', file=sys.stderr)


if __name__ == '__main__':
    app.debug=True
    socketio.run(app,host='localhost')