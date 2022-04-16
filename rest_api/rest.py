from flask_restful import reqparse, abort, Api, Resource
from .users_resources import UsersResource, UsersListResource

class RestAPI:
    def __init__(self, app):
        self.api = Api(app)
        self.api.add_resource(UsersListResource, '/api/v1/users')
        self.api.add_resource(UsersResource, '/api/v1/users/<int:user_id>')
