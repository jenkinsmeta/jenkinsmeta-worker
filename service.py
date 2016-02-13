from flask import Flask, send_file
from flask_restful import Resource, Api
from jenkins_caller import computers, queue, views, view
from jenkinsmeta_pb2 import computers_pb2, queue_pb2
import io

app = Flask(__name__)
api = Api(app)


class Serialize(object):
    def __init__(self, obj):
        pass

def serialize_computers(computers):
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

def serialize_queue(queue):
    proto_queue = queue_pb2.Queue()
    for job in queue:
        proto_job = proto_queue.job.add()
        proto_job.url = queue[job]['url']
        proto_job.in_queue_since = queue[job]['in_queue_since']
        proto_job.id = queue[job]['id']
        if 'why' in queue[job]:
            proto_job.why = queue[job]['why']
        if 'blocked' in queue[job]:
            proto_job.blocked = bool(queue[job]['blocked'])
    return proto_queue


def return404():
    abort(404, message="Resource not found")

class Computers(Resource):
    def get(self):
        print computers()
        return send_file(io.BytesIO(serialize_computers(computers()).SerializeToString()))


class Queue(Resource):
    def get(self):
        print queue()
        return send_file(io.BytesIO(serialize_queue(queue()).SerializeToString()))


class Views(Resource):
    def get(self):
        return views()

class View(Resource):
    def get(self, name):
        return view(name)


api.add_resource(Computers, '/computers')
api.add_resource(Queue, '/queue')
api.add_resource(Views, '/views')
api.add_resource(View, '/view/<name>')

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)

