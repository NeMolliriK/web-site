from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User
from flask import jsonify
from datetime import date


def abort_if_user_not_found(user_id):
    if not db_session.create_session().query(User).get(user_id):
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
        args = put_parser.parse_args()
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        if args['password']:
            user.set_password(args['password'])
        if args['surname']:
            user.surname = args['surname']
        if args['name']:
            user.name = args['name']
        if args['patronymic']:
            user.patronymic = args['patronymic']
        if args['email']:
            if db_sess.query(User).filter(User.email == args['email']).first():
                return jsonify({'Error': 'A user with this email already exists'})
            user.email = args['email']
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        return jsonify({'users': [user.to_dict(
            only=('id', 'surname', 'name', 'patronymic', 'email')) for user
            in db_session.create_session().query(User).all()]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == args['email']).first():
            return jsonify({'Error': 'A user with this email already exists'})
        user = User(surname=args['surname'], name=args['name'], patronymic=args['patronymic'], email=args['email'])
        user.set_password(args['password'])
        user.set_date(date(*map(int, args["date_of_birth"].split("-"))))
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('patronymic', required=True)
parser.add_argument('date_of_birth', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
put_parser = reqparse.RequestParser()
put_parser.add_argument('surname')
put_parser.add_argument('name')
put_parser.add_argument('patronymic')
put_parser.add_argument('email')
put_parser.add_argument('password')
