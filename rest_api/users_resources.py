from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User
from flask import jsonify

parser = reqparse.RequestParser()
parser.add_argument('id', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True, type=bool)
parser.add_argument('patronymic', required=True, type=bool)
parser.add_argument('age', required=True, type=int)
parser.add_argument('date_of_birth', required=True, type=int)
parser.add_argument('email', required=True, type=int)
parser.add_argument('employee', required=True, type=int)
parser.add_argument('student', required=True, type=int)


def abort_if_user_not_found(user_id):
    user = db_session.create_session().query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'User': user.to_dict(
            only=('id', 'surname', 'name', 'patronymic', 'date_of_birth', 'email', 'employee', 'student'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('id', 'email', 'employee', 'student')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            patronymic=args['patronymic'],
            date_of_birth=args['date_of_birth'],
            email=args['email'],
            hashed_password=args['hashed_password']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
