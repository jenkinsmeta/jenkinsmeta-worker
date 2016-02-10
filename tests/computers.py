from flask_restful import Resource, Api
from flask import Flask

return_computers = "\np\n\u0006master\u0010\u0002\u001a1\b\u0001\u0012\u0007keketki\u00183\"\"http://localhost:8080/job/keketki/\u001a1\b\u0001\u0012\u0007keketki\u00182\"\"http://localhost:8080/job/keketki/"

class JenkinsPoll(Resource):
    def get(self):
        return return_computers


app = Flask(__name__)
api = Api(app)


api.add_resource(JenkinsPoll, '/computers')

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)

