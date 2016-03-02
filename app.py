from flask_restful import Resource, Api, request
from flask_utils import ProtoFlask
import jenkins_worker
from api_factory import APIFactory

app = ProtoFlask(__name__)
api = Api(app)

#        Deserialization will be needed first, to check if payload is about jenkins or other
# curl --header "X-url: kekedserver:8080" -H "X-api: jenkins" http://127.0.0.1:5000/computers -X GET



class Computers(Resource):
##tutaj potrzebna jest fabryka na podstawie request.header api wywolywanie odpowiednich obiektow typu worker
    def get(self):
        return APIFactory(request.header).computers()
        #return jenkins_worker.serialize_computers(jenkins_worker.computers())

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

