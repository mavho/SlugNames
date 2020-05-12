from flask import render_template 
from SlugNames import app
from SlugNames.namesGenerator import generateNames
from SlugNames.RoomMaster import RoomMaster
import sys

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    thenames = generateNames()
    return render_template('layouts/index.html')

@app.route('/game', methods=['GET'])
def theGame():
    GM = RoomMaster()
    #thenames is a 5x5 2d list with the words for codenames 
    return render_template('layouts/game_room.html')