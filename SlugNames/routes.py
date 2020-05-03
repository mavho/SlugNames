from flask import render_template 
from SlugNames import app
from SlugNames.namesGenerator import generateNames

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    generateNames()
    return render_template('index.html')