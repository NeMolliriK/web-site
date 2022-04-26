from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User
from data.staff import Employee
from flask import jsonify
from datetime import date


def abort_if_employee_not_found(employee_id):
    if not db_session.create_session().query(Employee).get(employee_id):
        abort(404, message=f"Employee {employee_id} not found")


class StaffResource(Resource):
    def get(self, employee_id):
        abort_if_employee_not_found(employee_id)
        return jsonify({'employee': db_session.create_session().query(Employee).get(employee_id).to_dict(only=(
            'id', 'surname', 'name', 'patronymic', 'age', 'position', 'speciality', 'experience', 'address', 'email',
            'native_city', 'date_of_birth', 'class_'))})

    def delete(self, employee_id):
        abort_if_employee_not_found(employee_id)
        db_sess = db_session.create_session()
        employee = db_sess.query(Employee).get(employee_id)
        db_sess.delete(employee.user)
        db_sess.delete(employee)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, employee_id):
        args = put_parser.parse_args()
        abort_if_employee_not_found(employee_id)
        db_sess = db_session.create_session()
        employee = db_sess.query(Employee).get(employee_id)
        user = employee.user
        if args['surname']:
            employee.surname = user.surname = args['surname']
        if args['name']:
            employee.name = user.name = args['name']
        if args['patronymic']:
            employee.patronymic = user.patronymic = args['patronymic']
        if args['email']:
            if db_sess.query(User).filter(User.email == args['email']).first():
                return jsonify({'Error': 'A user with this email already exists.'})
            employee.email = user.email = args['email']
        if args['position']:
            employee.position = args['position']
        if args['speciality']:
            employee.speciality = args['speciality']
        if args['experience']:
            employee.experience = args['experience']
        if args['address']:
            employee.address = args['address']
        if args['class_']:
            if db_sess.query(Employee).filter(Employee.class_ == args['class_']).first():
                return jsonify({'Error': 'A class teacher has already been appointed for this class.'})
            employee.class_ = args['class_']
        if args['password']:
            user.set_password(args['password'])
        db_sess.commit()
        return jsonify({'success': 'OK'})


class StaffListResource(Resource):
    def get(self):
        return jsonify({'staff': [employee.to_dict(only=(
            'id', 'surname', 'name', 'patronymic', 'age', 'position', 'speciality', 'experience', 'address', 'email',
            'native_city', 'date_of_birth', 'class_')) for employee in
            db_session.create_session().query(Employee).all()]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == args['email']).first():
            return jsonify({'Error': 'A user with this email already exists.'})
        employee = Employee(surname=args['surname'], name=args['name'], patronymic=args['patronymic'],
                            position=args['position'], speciality=args['speciality'],
                            experience=args['experience'], address=args['address'], email=args['email'],
                            native_city=args['native_city'])
        employee.set_date(date(*map(int, args["date_of_birth"].split("-"))))
        if args["class_"]:
            if db_sess.query(Employee).filter(Employee.class_ == args['class_']).first():
                return jsonify({'Error': 'A class teacher has already been appointed for this class.'})
            employee.class_ = args['class_']
        user = User(surname=args['surname'], name=args['name'], patronymic=args['patronymic'], email=args['email'])
        user.set_password(args['password'])
        user.set_date(date(*map(int, args["date_of_birth"].split("-"))))
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
parser.add_argument('experience', required=True, type=int)
parser.add_argument('address', required=True)
parser.add_argument('class_')
parser.add_argument('date_of_birth', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
parser.add_argument('native_city', required=True)
put_parser = reqparse.RequestParser()
put_parser.add_argument('surname')
put_parser.add_argument('name')
put_parser.add_argument('patronymic')
put_parser.add_argument('position')
put_parser.add_argument('speciality')
put_parser.add_argument('experience', type=int)
put_parser.add_argument('address')
put_parser.add_argument('class_')
put_parser.add_argument('email')
put_parser.add_argument('password')
