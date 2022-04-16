from flask_restful import reqparse, abort, Api, Resource

class RestAPI:
    def __init__(self, app):
        self.api = Api(app)