from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, DateField
from wtforms.validators import InputRequired, EqualTo
from validators import AgeVerification


class AddWorker(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('password_again')])
    password_again = PasswordField('Confirm password', validators=[InputRequired()])
    surname = StringField('Surname', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    patronymic = StringField('Patronymic', validators=[InputRequired()])
    date_of_birth = DateField("Date of birth", validators=[InputRequired(), AgeVerification(16)])
    position = StringField('Position', validators=[InputRequired()])
    speciality = StringField('Speciality', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    native_city = StringField('Native city', validators=[InputRequired()])
    submit = SubmitField('Add an employee')


class EditWorker(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('password_again')])
    password_again = PasswordField('Confirm password', validators=[InputRequired()])
    surname = StringField('Surname', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    patronymic = StringField('Patronymic', validators=[InputRequired()])
    date_of_birth = DateField("Date of birth", validators=[InputRequired(), AgeVerification(16)])
    position = StringField('Position', validators=[InputRequired()])
    speciality = StringField('Speciality', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    native_city = StringField('Native city', validators=[InputRequired()])
    submit = SubmitField('Edit worker')
