from flask import Flask

@app.route("/")
def hello():
    return "I heart NY!"

@app.route('/index')
def index():
    return "Hello index"