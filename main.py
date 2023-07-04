from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import fun
app = Flask(__name__)
api = Api(app)

class Hello(Resource):
    def get(self):
        return jsonify({'message': 'hello world'})
  
    def post(self):
        data = request.get_json()     # status code
        return jsonify({'data': data}), 201

# another resource to calculate the square of a number
class Square(Resource):
  
    def get(self, num):
        return jsonify({'square': num**2})


api.add_resource(Hello, '/')
api.add_resource(Square, '/square/<int:num>')

if __name__ == '__main__':
    app.run(debug=True)     # runs the web server, debug true means any changes will be re-run