
#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.restful import reqparse
 
app = Flask(__name__, static_url_path = "")


#validation of querystring parameters
parser = reqparse.RequestParser()
parser.add_argument('year', type=int, required=True, location='args', help='year cannot be converted')
parser.add_argument('radius', type=int, required=True, location='args', help='Radius cannot be converted')

#error handlers
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
 
#base json response
response = {
    'most_likely_probability': 0.3,
    'p_interval_start': 0.2,
    'p_interval_end': 0.4,
    'inputs': {
        'year': 2013,
        'radius': 100,
        'latitude': 40.662670,
        'longitude': -73.908203,
        'start_time': '14:00',
        'duration': 60
    },
    'number_of_fines': 80,
    'number_of_periods': 365,
    'number_of_periods_with_fines': 42, # does not match probability, but never mind!
    'historical': [
        { 'lat': 40.662670, 'long': -73.908203, 'date': '2013-03-02' },
        { 'lat': 40.664764, 'long': -73.904900, 'date': '2013-05-03' },
        { 'lat': 40.690067, 'long': -73.991173, 'date': '2013-06-06' },
        { 'lat': 40.692677, 'long': -73.988159, 'date': '2013-07-01' }
    ]
}
 
#handle get request    
@app.route('/nyparking/api/v1.0/model', methods = ['GET'])
def get_model():
    args = parser.parse_args()
    response['inputs']['year']=args['year']
    response['inputs']['radius']=args['radius']
    return jsonify( { 'tasks': response } )
 

    
if __name__ == '__main__':
    app.run(debug = True)