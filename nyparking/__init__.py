from flask import Flask
# from nyparking import config

app = Flask(__name__)
app.config.from_pyfile('config.py')

import nyparking.views
