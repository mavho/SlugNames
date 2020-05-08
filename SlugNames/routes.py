from flask import render_template 
from SlugNames import app
from SlugNames.namesGenerator import generateNames
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('layouts/index.html')

@app.route('/game', methods=['GET'])
def theGame():
    thenames = generateNames()
    #thenames is a 5x5 2d list with the words for codenames 
    return render_template('thegame.html', thenames=thenames)