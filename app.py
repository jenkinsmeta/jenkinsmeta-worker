from flask_restful import Resource, Api, request
from flask_utils import ProtoFlask
from api_factory import APIFactory

app = ProtoFlask(__name__)
api = Api(app)

# curl -H "X-JenkinsMeta-URL: localhost:8080" -H "X-JenkinsMeta-API: Jenkins" http://127.0.0.1:5000/computers -X GET

class Computers(Resource):
    def get(self):
        return APIFactory(request.headers).computers()

class Queue(Resource):
    def get(self):
        return APIFactory(request.headers).queue()

class Views(Resource):
    def get(self):
        return APIFactory(request.headers).views()

class View(Resource):
    def get(self, name):
        return APIFactory(request.headers).view(name)




api.add_resource(Computers, '/computers')
api.add_resource(Queue, '/queue')
api.add_resource(Views, '/views')
api.add_resource(View, '/view/<name>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

