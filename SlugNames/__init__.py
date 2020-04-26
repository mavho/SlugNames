from flask import Flask
from config import Config
import os
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from SlugNames import routes