from flask import Flask, send_file
from flask_restful import Resource, Api
import jenkins_worker

app = Flask(__name__)
api = Api(app)



def return404():
    abort(404, message="Resource not found")

class Computers(Resource):
    def get(self):
        return jenkins_worker.serialize_computers(jenkins_worker.computers())


class Queue(Resource):
    def get(self):
        return jenkins_worker.serialize_queue(jenkins_worker.queue())


class Views(Resource):
    def get(self):
        return jenkins_worker.serialize_views(jenkins_worker.views())

class View(Resource):
    def get(self, name):
        return jenkins_worker.serialize_view(jenkins_worker.view(name))


api.add_resource(Computers, '/computers')
api.add_resource(Queue, '/queue')
api.add_resource(Views, '/views')
api.add_resource(View, '/view/<name>')

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)

