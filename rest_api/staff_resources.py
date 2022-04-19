from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User
from data.staff import Employee
from flask import jsonify
from datetime import date


def abort_if_employee_not_found(user_id):
    employee = db_session.create_session().query(Employee).get(user_id)
    if not employee:
        abort(404, message=f"Employee {user_id} not found")


class StaffResource(Resource):
    def get(self, user_id):
        abort_if_employee_not_found(user_id)
        return jsonify({'employee': db_session.create_session().query(Employee).get(user_id).to_dict()})

    def delete(self, user_id):
        abort_if_employee_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(Employee).get(user_id)['user']

        db_sess.delete(user)
        db_sess.delete(db_sess.query(Employee).get(user_id))
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        args = put_parser.parse_args()
        abort_if_employee_not_found(user_id)
        db_sess = db_session.create_session()
        employee = db_sess.query(Employee).get(user_id)
        user = db_sess.query(Employee).get(user_id)['user']
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
        if 'position' in args:
            employee.email = args['position']
        if 'speciality' in args:
            employee.email = args['speciality']
        if 'experience' in args:
            employee.email = args['experience']
        if 'address' in args:
            employee.email = args['address']
        if 'classroom_teacher' in args:
            employee.email = args['classroom_teacher']
        if 'class_' in args:
            employee.email = args['class_']

        if 'password' in args:
            user.set_password(args['password'])

        db_sess.commit()
        return jsonify({'success': 'OK'})


class StaffListResource(Resource):
    def get(self):
        return jsonify({'staff': [user.to_dict(
            only=('id', 'surname', 'name', 'patronymic', 'age', 'date_of_birth', 'email', 'hashed_password')) for user
            in db_session.create_session().query(Employee).all()]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        employee = Employee(surname=args['surname'], name=args['name'], patronymic=args['patronymic'],
                            position=args['position'], speciality=args['speciality'],
                            experience=args['experience'], address=args['address'], email=args['email'],
                            native_city=args['native_city'])
        employee.set_date(args['date_of_birth'])
        if 'classroom_teacher' in args:
            employee.class_ = args['class_']
        user = User(surname=args['surname'], name=args['name'], patronymic=args['patronymic'], email=args['email'])
        user.set_password(args['password'])
        user.set_date(args['date_of_birth'])
        db_sess.add(employee)
        db_sess.add(user)
        db_sess.commit()

        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('patronymic', required=True)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('experience', required=True)
parser.add_argument('address', required=True)
parser.add_argument('classroom_teacher', required=False)
parser.add_argument('class_', required=False)
parser.add_argument('date_of_birth', required=True, type=date)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)

put_parser = reqparse.RequestParser()
put_parser.add_argument('surname')
put_parser.add_argument('name')
put_parser.add_argument('patronymic')
put_parser.add_argument('position')
put_parser.add_argument('speciality')
put_parser.add_argument('experience')
put_parser.add_argument('address')
put_parser.add_argument('classroom_teacher')
put_parser.add_argument('class_', )
put_parser.add_argument('email')
put_parser.add_argument('password')
