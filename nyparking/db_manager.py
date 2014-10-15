from nyparking import app
import psycopg2
from flask import g
import datetime

def get_db():
    # print "get_db"
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(app.config['PSYCOPG2_CONNECT_STRING'])
    return db

def get_db_cursor():
    return get_db().cursor()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
