from flask import render_template 
from SlugNames import app

@app.route('/index')
def index():
    return('route defs')