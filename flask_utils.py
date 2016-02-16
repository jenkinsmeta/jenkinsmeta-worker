from flask import Flask, Response

class ProtoResponse(Response):
    default_mimetype = 'application/octet-stream'
    def __init__(self, response, **kwargs):
        response = response.SerializeToString()
        super(ProtoResponse, self).__init__(response, **kwargs)

class ProtoFlask(Flask):
    response_class = ProtoResponse
