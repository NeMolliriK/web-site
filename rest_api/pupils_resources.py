from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User
from data.pupils import Student
from flask import jsonify
from datetime import date


def abort_if_student_not_found(user_id):
    employee = db_session.create_session().query(Student).get(user_id)
    if not employee:
        abort(404, message=f"Student {user_id} not found")


class StaffResource(Resource):
    def get(self, user_id):
        abort_if_student_not_found(user_id)
        return jsonify({'student': db_session.create_session().query(Student).get(user_id).to_dict()})

    def delete(self, user_id):
        abort_if_student_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(Student).get(user_id)['user']

        db_sess.delete(user)
        db_sess.delete(db_sess.query(Student).get(user_id))
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        args = put_parser.parse_args()
        abort_if_student_not_found(user_id)
        db_sess = db_session.create_session()
        employee = db_sess.query(Student).get(user_id)
        user = db_sess.query(Student).get(user_id)['user']
        if 'surname' in args:
            employee.surname = args['surname']
            user.surname = args['surname']
        if 'name' in args:
            employee.name = args['name']
            user.name = args['name']
        if 'patronymic' in args:
            employee.patronymic = args['patronymic']
            user.patronymic = args['patronymic']
        if 'email' in args:
            employee.email = args['email']
            user.email = args['email']
        if 'address' in args:
            employee.address = args['address']
        if 'native_city' in args:
            employee.native_city = args['native_city']
        if 'class_' in args:
            employee.class_ = args['class_']

        if 'password' in args:
            user.set_password(args['password'])

        db_sess.commit()
        return jsonify({'success': 'OK'})


class StaffListResource(Resource):
    def get(self):
        return jsonify({'staff': [user.to_dict(
            only=('id', 'surname', 'name', 'patronymic', 'age', 'date_of_birth', 'email', 'hashed_password')) for user
            in db_session.create_session().query(Student).all()]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        student = Student(surname=args['surname'], name=args['name'], patronymic=args['patronymic'],
                          address=args['address'], email=args['email'], native_city=args['native_city'],
                          class_=args['class_'] if c else current_user.employee.class_)
        user = User(surname=args['surname'], name=args['name'], patronymic=args['patronymic'],
                    email=args['email'])
        student.set_date(args['date_of_birth'])
        user.set_password(args['password'])
        user.set_date(args['date_of_birth'])
        db_sess.add(student)
        db_sess.add(user)
        db_sess.commit()

        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('patronymic', required=True)
parser.add_argument('address', required=True)
parser.add_argument('classroom_teacher')
parser.add_argument('native_city')
parser.add_argument('class_')
parser.add_argument('date_of_birth', required=True, type=date)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)

put_parser = reqparse.RequestParser()
parser.add_argument('surname')
parser.add_argument('name')
parser.add_argument('patronymic')
parser.add_argument('address')
parser.add_argument('classroom_teacher')
parser.add_argument('native_city')
parser.add_argument('class_')
parser.add_argument('email')
parser.add_argument('password')
