from flask import Flask
from flask_restful import Resource, Api
from jenkins_caller import queue


app = Flask(__name__)
api = Api(app)



def return404():
    abort(404, message="Resource not found")

class JenkinsPoll(Resource):
    def get(self):
        return queue() 


api.add_resource(JenkinsPoll, '/queue')

if __name__ == '__main__':
        app.run(debug=True)

