from flask import Flask, send_file
from flask_restful import Resource, Api
from jenkins_caller import computers, queue, views
from jenkinsmeta_pb2 import computers_pb2
import io

app = Flask(__name__)
api = Api(app)


class Serialize(object):
    def __init__(self, obj):
        pass

def serialize(computers):
    proto_computers = computers_pb2.Computers()
    for computer in computers:
        proto_computer = proto_computers.computer.add()
        proto_computer.name = computer
        proto_computer.executors = computers[computer]['executors']
        for job in computers[computer]['jobs_active']:
            proto_job = proto_computer.job.add()
            proto_job.state = 1
            proto_job.name = job['name']
            proto_job.build_number = int(job['number'])
            proto_job.url =  job['url']
            if 'duration' in job:
                proto_job.duration = job['duration']
            if 'estimated_duration' in job:
                proto_job.estimated_duration = job['estimated_duration']
    return proto_computers


def return404():
    abort(404, message="Resource not found")

class Computers(Resource):
    def get(self):
        return send_file(io.BytesIO(serialize(computers()).SerializeToString()))


class Queue(Resource):
    def get(self):
        return queue()


class Views(Resource):
    def get(self):
        return views()





api.add_resource(Computers, '/computers')
api.add_resource(Queue, '/queue')
api.add_resource(Views, '/views')

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)

