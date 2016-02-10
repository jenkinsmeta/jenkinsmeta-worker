from flask import Flask
from flask_restful import Resource, Api
from jenkins_caller import executors


app = Flask(__name__)
api = Api(app)



def return404():
    abort(404, message="Resource not found")

class JenkinsPoll(Resource):
    def get(self):
        return executors() 


api.add_resource(JenkinsPoll, '/executors')

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)

