
#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.restful import reqparse
 
app = Flask(__name__, static_url_path = "")

parser = reqparse.RequestParser()
parser.add_argument(
    'year', dest='year',
    type=str, location='args',
    required=False, help='The user\'s username',
)
args = parser.parse_args()



@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
 
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

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
 
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
        else:
            new_task[field] = task[field]
    return new_task
    
@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return jsonify( { 'tasks': response } )
 
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    response['most_likely_probability']=task_id
    return jsonify( { 'task': response } )
 
@app.route('/todo/api/v1.0/tasks', methods = ['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify( { 'task': make_public_task(task) } ), 201
 
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify( { 'task': make_public_task(task[0]) } )
    
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(debug = True)