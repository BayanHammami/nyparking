from flask import Flask


@app.route("/")
def hello():
    return "I heart NY!"


@app.route('/getheatmap', methods = ['GET'])
def api_getheatmap():
    data = {
        'hello'  : 'world',
        'number' : 3
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://luisrei.com'

    return resp


app = Flask(__name__)

if __name__ == "__main__":
    app.run()