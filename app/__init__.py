from flask import Flask, request
from flask.ext.restful import Resource, Api

app = Flask(__name__)
api = Api(app)

samle_data = {}

class GetData(Resource):
    def get(self, item_id):
        return {item_id: samle_data[item_id]}


api.add_resource(GetData, '/<string:item_id>')

if __name__ == '__main__':
    app.run(debug=True)