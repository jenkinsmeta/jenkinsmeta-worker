from flask_restful import Resource, Api, request
from flask_utils import ProtoFlask
from api_factory import get_api

app = ProtoFlask(__name__)
api = Api(app)

# curl -H "X-JenkinsMeta-URL: localhost:8080" -H "X-JenkinsMeta-API: Jenkins" http://127.0.0.1:5000/computers -X GET

class Computers(Resource):
    def get(self):
        url = request.headers.get('X-JenkinsMeta-URL')
        api = get_api(request)
        return api.computers(url)

class Queue(Resource):
    def get(self):
        url = request.headers.get('X-JenkinsMeta-URL')
        api = get_api(request)
        return api.queue(url)

class Views(Resource):
    def get(self):
        url = request.headers.get('X-JenkinsMeta-URL')
        api = get_api(request)
        return api.views()

class View(Resource):
    def get(self, name):
        url = request.headers.get('X-JenkinsMeta-URL')
        api = get_api(request)
        return api.view(url, name)




api.add_resource(Computers, '/computers')
api.add_resource(Queue, '/queue')
api.add_resource(Views, '/views')
api.add_resource(View, '/view/<name>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

