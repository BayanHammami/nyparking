from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

@app.route('/getdata', methods=['GET'])
def get_estimates():
    print request.args.get('year')
    print request.args.get('radius')
    print request.args.get('latitude')
    print request.args.get('longitude')    
    print request.args.get('start_time')
    print request.args.get('duration')

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
    'number_of_periods_with_fines': 42, 
    'historical': [
        { 'lat': 40.662670, 'long': -73.908203, 'date': '2013-03-02' },
        { 'lat': 40.664764, 'long': -73.904900, 'date': '2013-05-03' },
        { 'lat': 40.690067, 'long': -73.991173, 'date': '2013-06-06' },
        { 'lat': 40.692677, 'long': -73.988159, 'date': '2013-07-01' }
    ]
}

@app.route('/prob', methods=['GET'])
def get_prob():
    return jsonify({'prob': response})

if __name__ == "__main__":
    app.run()
