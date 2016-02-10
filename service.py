from flask import Flask
from flask_restful import Resource, Api
from jenkins_caller import executors
from jenkinsmeta_pb2 import computers_pb2


app = Flask(__name__)
api = Api(app)


def serialize(computers):
    proto_computers = computers_pb2.Computers()
    for computer in computers:
        proto_computer = proto_computers.computer.add()
        proto_computer.name = computer
        print(computers[computer])
        proto_computer.executors = computers[computer]['executors']
        for job in computers[computer]['jobs_active']:
            proto_job = proto_computer.job.add()
            proto_job.state = 1
            proto_job.name = job['name']
            print(job['number'])
            proto_job.build_number = int(job['number'])
            proto_job.url =  job['url']

    return proto_computers


def return404():
    abort(404, message="Resource not found")

class JenkinsPoll(Resource):
    def get(self):
        return serialize(executors()).SerializeToString()


api.add_resource(JenkinsPoll, '/computers')

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)

