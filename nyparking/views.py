from nyparking import app, risk_assessor

import psycopg2

from flask import jsonify, abort, request, make_response, url_for, g

from datetime import datetime
from datetime import time
import time
from db_manager import get_db_cursor

#error handlers
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
 
# #base json response
# response = {
#     'number_of_fines': 0,
#     'number_of_dates_with_fines': 0,
#     'number_of_possible_dates': 0,
#     'inputs': {
#         'data_set': 0,
#         'start_time': '',
#         'lat': 0,
#         'lng': 0,
#         'duration': 0,
#         'radius': 0
#     },
#     'most_likely_probability': 0,
#     'probability_interval': 0,
#     'historical_sample': [
#         { 'lat': 40.662670, 'lng': -73.908203, 'time': '00:00' },
#         { 'lat': 40.692677, 'lng': -73.988159, 'time': '00:00' }
#     ]
# }
 
def get_summary_pg():
    result = db.session.query().from_statement('select * from app_summary_vw').all()
    #result = db.engine.execute('SELECT app_model_summary_sp(?,?,?)', 1, 2, 3).fetchall()

    return result

def run_model(args):
    get_summary_pg()
    
    #relay back the request
    response['inputs']['data_set']=args['data_set']
    response['inputs']['start_time']=args['start_time']
    response['inputs']['duration']=args['duration']
    response['inputs']['radius']=args['radius']
    response['inputs']['lat']=args['lat']
    response['inputs']['lng']=args['lng']
    return response

@app.route('/nyparking/db_test', methods = ['GET'])
def db_test():
    cursor = get_db_cursor()

    return "Connection established."

@app.route('/nyparking/num_days')
def get_number_of_valid_weekdays():
    return str(risk_assessor.number_of_valid_weekdays)

@app.route('/nyparking/request_echo', methods = ['GET'])
def run_request_echo():
    return jsonify(request.args.to_dict())

@app.route('/nyparking/assess_risk', methods = ['GET'])
def assess_risk():
    args = request.args.to_dict()

    print args

    # try:
    lat = float(args['lat'])
    lng = float(args['lng'])
    # start_time = time.strptime(args['time'], '%H:%M')
    start_time = datetime.strptime(args['time'], '%H:%M').time()

    duration = int(args['duration'])
    data_set = int(args['year_option'])
    radius = int(args['circleradius'])
    # except Exception e:
    #     return "Except"

    # return jsonify([lat, lng, radius, start_time, duration, data_set, True, True])

    return jsonify(risk_assessor.main(lat, lng, radius, start_time, duration, data_set, True, True))

@app.route('/nyparking/assess_risk_test', methods = ['GET'])
def assess_risk_test():
    return jsonify(risk_assessor.main(40.725671, -73.984719, 150, datetime.now().time(), 60*3, 2013, True, True))

#handle get request    
@app.route('/nyparking/api/v1.0/model', methods = ['GET'])
def get_model():
    args = parser.parse_args()  

    return jsonify( { 'tasks': run_model(args) } )
    
# if __name__ == '__main__':
#     app.run(debug = True)