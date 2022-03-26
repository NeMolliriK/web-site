from os import environ
from flask import Flask, render_template, redirect
from flask_login import login_required, logout_user, LoginManager, login_user
from data import db_session
from forms.authorization import LoginForm
from forms.registration import RegisterForm
from data.users import User
from waitress import serve

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ijB9sBTlZaOFFj1YB{'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/school.db")
db_sess = db_session.create_session()


@app.route('/')
def base():
    return render_template("base.html", title="Main page")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Registration', form=form,
                                   message="Passwords do not match", registration=1)
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Registration', form=form,
                                   message="This user already exists", registration=1)
        user = User(surname=form.surname.data, name=form.name.data, patronymic=form.patronymic.data,
                    date_of_birth=form.date_of_birth.data, email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
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


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=int(environ.get("PORT", 5000)))
