from flask_restful import Resource, Api, request
from flask_utils import ProtoFlask
import jenkins_worker

app = ProtoFlask(__name__)
api = Api(app)

#        curl --data "127.0.0.1:8080" http://127.0.0.1:5000/computers -X POST -H "Content-Type:application/octet-stream"
#        curl --data "127.0.0.1:8080" http://127.0.0.1:5000/view/shorttime -X POST -H "Content-Type:application/octet-stream"
#        curl --data "127.0.0.1:8080" http://127.0.0.1:5000/views -X POST -H "Content-Type:application/octet-stream"
#        curl --data "127.0.0.1:8080" http://127.0.0.1:5000/queue -X POST -H "Content-Type:application/octet-stream"
#        Deserialization will be needed first, to check if payload is about jenkins or other



class Computers(Resource):
    def post(self):
        return jenkins_worker.serialize_computers(jenkins_worker.computers(request.get_data()))

class Queue(Resource):
    def post(self):
        return jenkins_worker.serialize_queue(jenkins_worker.queue(request.get_data()))

class Views(Resource):
    def post(self):
        return jenkins_worker.serialize_views(jenkins_worker.views(request.get_data()))

class View(Resource):
    def post(self, name):
        return jenkins_worker.serialize_view(jenkins_worker.view(request.get_data(), name))




api.add_resource(Computers, '/computers')
api.add_resource(Queue, '/queue')
api.add_resource(Views, '/views')
api.add_resource(View, '/view/<name>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

