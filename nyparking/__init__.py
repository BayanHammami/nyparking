from flask import Flask
# from nyparking import config

app = Flask(__name__, static_folder = 'static', static_url_path = '')
app.config.from_pyfile('config.py')

import nyparking.views
