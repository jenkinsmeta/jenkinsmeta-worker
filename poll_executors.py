from flask import Flask
from flask_restful import Resource, Api



app = Flask(__name__)
api = Api(app)


api.add_resource(, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

def return404():
    abort(404, message="Resource not found")

class JenkinsPoll(Resource):
    def get(self)





