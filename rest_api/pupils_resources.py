from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User
from data.pupils import Student
from flask import jsonify
from datetime import date
from modules import key


def check_api_key():
    add_args = put_parser.parse_args()
    if not key.check_key(add_args['key']):
        abort(404, message=f"Error: No valid API key provided")
        return False
    return True


def abort_if_student_not_found(student_id):
    employee = db_session.create_session().query(Student).get(student_id)
    if not employee:
        abort(404, message=f"Student {student_id} not found")


class StudentResource(Resource):
    def get(self, student_id):
        if not check_api_key():
            return
        abort_if_student_not_found(student_id)
        return jsonify(
            {'student': db_session.create_session().query(Student).get(student_id).to_dict(only=(
                'id', 'surname', 'name', 'patronymic', 'age', 'class_', 'address', 'email', 'native_city',
                'date_of_birth'))})

    def delete(self, student_id):
        if not check_api_key():
            return
        abort_if_student_not_found(student_id)
        db_sess = db_session.create_session()
        user = db_sess.query(Student).get(student_id).user
        db_sess.delete(user)
        db_sess.delete(db_sess.query(Student).get(student_id))
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, student_id):
        if not check_api_key():
            return
        args = put_parser.parse_args()
        abort_if_student_not_found(student_id)
        db_sess = db_session.create_session()
        student = db_sess.query(Student).get(student_id)
        user = db_sess.query(Student).get(student_id).user
        if 'surname' in args:
            student.surname = args['surname']
            user.surname = args['surname']
        if 'name' in args:
            student.name = args['name']
            user.name = args['name']
        if 'patronymic' in args:
            student.patronymic = args['patronymic']
            user.patronymic = args['patronymic']
        if 'email' in args:
            student.email = args['email']
            user.email = args['email']
        if 'address' in args:
            student.address = args['address']
        if 'native_city' in args:
            student.native_city = args['native_city']
        if 'class_' in args:
            student.class_ = args['class_']
        if 'password' in args:
            user.set_password(args['password'])
        db_sess.commit()
        return jsonify({'success': 'OK'})


class StudentListResource(Resource):
    def get(self):
        if not check_api_key():
            return
        return jsonify({'pupils': [student.to_dict(only=(
            'id', 'surname', 'name', 'patronymic', 'age', 'class_', 'address', 'email', 'native_city', 'date_of_birth'))
            for
            student in db_session.create_session().query(Student).all()]})

    def post(self):
        if not check_api_key():
            return
        args = parser.parse_args()
        db_sess = db_session.create_session()
        student = Student(surname=args['surname'], name=args['name'], patronymic=args['patronymic'],
                          address=args['address'], email=args['email'], native_city=args['native_city'],
                          class_=args['class_'])
        user = User(surname=args['surname'], name=args['name'], patronymic=args['patronymic'], email=args['email'])
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
parser.add_argument('native_city', required=True)
parser.add_argument('class_', required=True)
parser.add_argument('date_of_birth', required=True, type=date)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
put_parser = reqparse.RequestParser()
parser.add_argument('surname')
parser.add_argument('name')
parser.add_argument('patronymic')
parser.add_argument('address')
parser.add_argument('native_city')
parser.add_argument('class_')
parser.add_argument('email')
parser.add_argument('password')
put_parser.add_argument('key', required=True)
