from os import environ
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request
from flask_login import login_required, logout_user, LoginManager, login_user, current_user
from data import db_session
from data.staff import Employee
from forms.authorization import LoginForm
from forms.registration import RegisterForm
from data.users import User
from waitress import serve
from forms.staff import AddEmployee, EditEmployee
from mail_sender import send_email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ijB9sBTlZaOFFj1YB{'
login_manager = LoginManager()
login_manager.init_app(app)
load_dotenv()
db_session.global_init("db/school.sqlite")
db_sess = db_session.create_session()


@app.route('/')
def base():
    return render_template("base.html", title="Main page")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Registration', form=form,
                                   message="This user already exists", registration=1)
        user = User(surname=form.surname.data, name=form.name.data, patronymic=form.patronymic.data,
                    email=form.email.data)
        send_email(form.email.data, "Thank you for registering!",
                   "Thank you very much for registering on our site! Hope we don't disappoint you!\nBest regards, our w"
                   "ebsite team.", ["static/img/thank_you_for_registering.png"])
        user.set_password(form.password.data)
        user.set_date(form.date_of_birth.data)
        db_sess.add(user)
        db_sess.commit()
        if current_user.is_authenticated:
            return redirect('/logout')
        return redirect('/login')
    return render_template('registration.html', title='Registration', form=form, registration=1)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('authorization.html', message="Incorrect login or password", form=form,
                               title="Authorization", authorization=1)
    return render_template('authorization.html', title='Authorization', form=form, authorization=1)


@app.route('/staff')
def staff():
    return render_template("staff.html", title="School staff", staff=db_sess.query(Employee),
                           director=1 if current_user.is_authenticated and current_user.id == 1 else 0)


@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    if current_user.is_authenticated and current_user.id != 1:
        return render_template("not_enough_rights.html", add_employee=1, title="Not enough rights")
    form = AddEmployee()
    if form.validate_on_submit():
        if db_sess.query(User).filter(User.email == form.email.data).first() or db_sess.query(Employee).filter(
                Employee.email == form.email.data).first():
            return render_template('add_employee.html', title='Adding an employee', form=form,
                                   message="The person with this email is already registered", add_employee=1)
        if form.classroom_teacher.data and db_sess.query(Employee).filter(Employee.class_ == form.class_.data).first():
            return render_template("add_employee.html", title='Adding an employee', add_employee=1, form=form,
                                   message="The class teacher for this class already exists")
        employee = Employee(surname=form.surname.data, name=form.name.data, patronymic=form.patronymic.data,
                            position=form.position.data, speciality=form.speciality.data,
                            experience=form.experience.data, address=form.address.data, email=form.email.data,
                            native_city=form.native_city.data)
        employee.set_date(form.date_of_birth.data)
        if form.classroom_teacher.data:
            employee.class_ = form.class_.data
        user = User(surname=form.surname.data, name=form.name.data, patronymic=form.patronymic.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        user.set_date(form.date_of_birth.data)
        db_sess.add(employee)
        db_sess.add(user)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/staff')
    return render_template("add_employee.html", title='Adding an employee', add_employee=1, form=form)


@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    form = EditEmployee()
    employee = db_sess.query(Employee).get(id)
    if request.method == "GET":
        form.email.data = employee.email
        form.surname.data = employee.surname
        form.name.data = employee.name
        form.patronymic.data = employee.patronymic
        form.position.data = employee.position
        form.speciality.data = employee.speciality
        form.experience.data = employee.experience
        form.classroom_teacher.data = bool(employee.class_)
        form.class_.data = employee.class_
        form.address.data = employee.address
    if form.validate_on_submit():
        user = employee.user
        if db_sess.query(User).filter(User.email == form.email.data).first() != user:
            return render_template('edit_employee.html', title='Editing an employee', form=form,
                                   message="The person with this email already exists", edit_employee=1)
        if form.classroom_teacher.data and db_sess.query(Employee).filter(
                Employee.class_ == form.class_.data).first() != employee:
            return render_template("edit_employee.html", title='Editing an employee', edit_employee=1, form=form,
                                   message="The class teacher for this class already exists")
        employee.email = user.email = form.email.data
        employee.surname = user.surname = form.surname.data
        employee.name = user.name = form.name.data
        employee.patronymic = user.patronymic = form.patronymic.data
        employee.position = form.position.data
        employee.speciality = form.speciality.data
        employee.experience = form.experience.data
        employee.address = form.address.data
        if form.classroom_teacher.data:
            employee.class_ = form.class_.data
        user.set_password(form.password.data)
        db_sess.commit()
        return redirect('/staff')
    return render_template('edit_employee.html', title='Editing an employee', form=form, edit_employee=1)


@app.route('/delete_an_employee/<int:id>')
@login_required
def delete_an_employee(id):
    employee = db_sess.query(Employee).get(id)
    db_sess.delete(employee.user)
    db_sess.delete(employee)
    db_sess.commit()
    return redirect('/staff')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


@app.errorhandler(401)
def unauthorized(error):
    return render_template("unauthorized.html")


@app.errorhandler(403)
def not_enough_rights(error):
    return render_template("not_enough_rights.html")


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=int(environ.get("PORT", 5000)))
