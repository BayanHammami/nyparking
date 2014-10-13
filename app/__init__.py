
#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.restful import reqparse
from flask.ext.sqlalchemy import SQLAlchemy
 
app = Flask(__name__, static_url_path = "")
#app.config.from_pyfile(config.py)
#db = SQLAlchemy(app)

#validation of querystring parameters
parser = reqparse.RequestParser()
parser.add_argument('data_set', type=str, required=True, location='args')
parser.add_argument('start_time', type=str, required=True, location='args')
parser.add_argument('duration', type=int, required=True, location='args')
parser.add_argument('radius', type=int, required=True, location='args')
parser.add_argument('lat', type=str, required=True, location='args')
parser.add_argument('lng', type=str, required=True, location='args', help='long cannot be converted')


#error handlers
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
 
#base json response
response = {
    'number_of_fines': 0,
    'number_of_dates_with_fines': 0,
    'number_of_possible_dates': 0,
    'inputs': {
        'data_set': 0,
        'start_time': '',
        'lat': 0,
        'lng': 0,
        'duration': 0,
        'radius': 0
    },
    'most_likely_probability': 0,
    'probability_interval': 0,
    'historical_sample': [
        { 'lat': 40.662670, 'lng': -73.908203, 'time': '00:00' },
        { 'lat': 40.692677, 'lng': -73.988159, 'time': '00:00' }
    ]
}
 
def run_model(args):
    #relay back the request
    response['inputs']['data_set']=args['data_set']
    response['inputs']['start_time']=args['start_time']
    response['inputs']['duration']=args['duration']
    response['inputs']['radius']=args['radius']
    response['inputs']['lat']=args['lat']
    response['inputs']['lng']=args['lng']
    return response

#handle get request    
@app.route('/nyparking/api/v1.0/model', methods = ['GET'])
def get_model():
    args = parser.parse_args()
    return jsonify( { 'tasks': run_model(args) } )
 

    
if __name__ == '__main__':
    app.run(debug = True)