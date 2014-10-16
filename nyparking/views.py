from nyparking import app, risk_assessor

import psycopg2
from flask import send_from_directory, jsonify, abort, request, make_response, url_for, g

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

@app.route('/nyparking/db_test', methods = ['GET'])
def db_test():
    cursor = get_db_cursor()
    return "Connection established."

@app.route('/nyparking/weekday_counts')
def get_weekday_counts():
    return jsonify(risk_assessor.weekday_counts)

@app.route('/nyparking/date_ranges')
def get_date_ranges():
    return jsonify(risk_assessor.date_ranges)

@app.route('/nyparking/time_distribution')
def get_time_distribution():
    args = request.args.to_dict()

    lat = float(args['lat'])
    lng = float(args['lng'])
    start_time = datetime.strptime(args['time'], '%H:%M').time()

    duration = int(args['duration'])
    radius = int(args['circleradius'])

    day_of_week = datetime.now().strftime('%A');

    distribution = risk_assessor.get_time_distribution(lat, lng, radius, 2013, day_of_week)
    return jsonify({
        'description': 'The total number of fines over the past four %ss broken down by time of day (hour beginning). The strange format is for Google charts compatibility.' % day_of_week,
        'time_distribution': distribution
    })


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

