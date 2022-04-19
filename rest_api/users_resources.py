from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User
from flask import jsonify
from datetime import date


def abort_if_user_not_found(user_id):
    user = db_session.create_session().query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        return jsonify({'user': db_session.create_session().query(User).get(user_id).to_dict(
            only=('id', 'surname', 'name', 'patronymic', 'age', 'date_of_birth', 'email', 'hashed_password'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        db_sess.delete(db_sess.query(User).get(user_id))
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        args = parser.parse_args()
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        if 'password' in args:
            user.set_password(args['password'])
        if 'date_of_birth' in args:
            user.set_date(args["date_of_birth"])
        if 'surname' in args:
            user.surname = args['surname']
        if 'name' in args:
            user.name = args['name']
        if 'patronymic' in args:
            user.patronymic = args['patronymic']
        if 'email' in args:
            user.email = args['email']
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        return jsonify({'users': [user.to_dict(
            only=('id', 'surname', 'name', 'patronymic', 'age', 'date_of_birth', 'email', 'hashed_password')) for user
            in db_session.create_session().query(User).all()]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        user = User(surname=args['surname'], name=args['name'], patronymic=args['patronymic'], email=args['email'])
        user.set_password(args['password'])
        user.set_date(args["date_of_birth"])
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('patronymic', required=True)
parser.add_argument('date_of_birth', required=True, type=date)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
