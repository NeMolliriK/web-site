from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User
from data.pupils import Student
from data.staff import Employee
from flask import jsonify
from datetime import date


def abort_if_student_not_found(student_id):
    if not db_session.create_session().query(Student).get(student_id):
        abort(404, message=f"Student {student_id} not found")


class PupilsResource(Resource):
    def get(self, student_id):
        abort_if_student_not_found(student_id)
        return jsonify(
            {'student': db_session.create_session().query(Student).get(student_id).to_dict(only=(
                'id', 'surname', 'name', 'patronymic', 'age', 'class_', 'address', 'email', 'native_city',
                'date_of_birth'))})

    def delete(self, student_id):
        abort_if_student_not_found(student_id)
        db_sess = db_session.create_session()
        student = db_sess.query(Student).get(student_id)
        db_sess.delete(student.user)
        db_sess.delete(student)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, student_id):
        args = put_parser.parse_args()
        abort_if_student_not_found(student_id)
        db_sess = db_session.create_session()
        student = db_sess.query(Student).get(student_id)
        user = student.user
        if args['surname']:
            student.surname = user.surname = args['surname']
        if args['name']:
            student.name = user.name = args['name']
        if args['patronymic']:
            student.patronymic = user.patronymic = args['patronymic']
        if args['email']:
            if db_sess.query(User).filter(User.email == args['email']).first():
                return jsonify({'Error': 'A user with this email already exists.'})
            student.email = user.email = args['email']
        if args['address']:
            student.address = args['address']
        if args['class_']:
            if not db_sess.query(Employee).filter(Employee.class_ == args["class_"]).first():
                return jsonify({'Error': 'A class teacher has not yet been appointed for this class.'})
            student.class_ = args['class_']
        if args['password']:
            user.set_password(args['password'])
        db_sess.commit()
        return jsonify({'success': 'OK'})


class PupilsListResource(Resource):
    def get(self):
        return jsonify({'pupils': [student.to_dict(only=(
            'id', 'surname', 'name', 'patronymic', 'age', 'class_', 'address', 'email', 'native_city', 'date_of_birth'))
            for
            student in db_session.create_session().query(Student).all()]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == args['email']).first():
            return jsonify({'Error': 'A user with this email already exists.'})
        if not db_sess.query(Employee).filter(Employee.class_ == args["class_"]).first():
            return jsonify({'Error': 'A class teacher has not yet been appointed for this class.'})
        student = Student(surname=args['surname'], name=args['name'], patronymic=args['patronymic'],
                          address=args['address'], email=args['email'], native_city=args['native_city'],
                          class_=args['class_'])
        user = User(surname=args['surname'], name=args['name'], patronymic=args['patronymic'], email=args['email'])
        student.set_date(date(*map(int, args["date_of_birth"].split("-"))))
        user.set_password(args['password'])
        user.set_date(date(*map(int, args["date_of_birth"].split("-"))))
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
parser.add_argument('date_of_birth', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
put_parser = reqparse.RequestParser()
put_parser.add_argument('surname')
put_parser.add_argument('name')
put_parser.add_argument('patronymic')
put_parser.add_argument('address')
put_parser.add_argument('native_city')
put_parser.add_argument('class_')
put_parser.add_argument('email')
put_parser.add_argument('password')
