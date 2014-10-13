from flask import Flask, jsonify


@app.route("/")
def hello():
    return "I heart NY!"


@app.route('/getheatmap', methods = ['GET'])
def api_getheatmap():
    data = {
        'hello'  : 'world',
        'number' : 1
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://pvpc0linapp002.demo.servian.com'

    return resp


app = Flask(__name__)

if __name__ == "__main__":
    app.run()