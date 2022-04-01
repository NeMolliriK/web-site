from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, DateField
from wtforms.validators import InputRequired, EqualTo
from .validators import AgeVerification, ClassCorrectness


class AddStudent(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    password_again = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password')])
    surname = StringField('Surname', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    patronymic = StringField('Patronymic', validators=[InputRequired()])
    date_of_birth = DateField("Date of birth", validators=[InputRequired(), AgeVerification(6)])
    class_ = StringField('Class', validators=[InputRequired(), ClassCorrectness()])
    address = StringField('Address', validators=[InputRequired()])
    native_city = StringField('Native city', validators=[InputRequired()])
    submit = SubmitField('Add student')


class EditStudent(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    password_again = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password')])
    surname = StringField('Surname', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    patronymic = StringField('Patronymic', validators=[InputRequired()])
    class_ = StringField('Class', validators=[InputRequired(), ClassCorrectness()])
    address = StringField('Address', validators=[InputRequired()])
    submit = SubmitField('Edit student')


class AddStudentWithoutClass(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    password_again = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password')])
    surname = StringField('Surname', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    patronymic = StringField('Patronymic', validators=[InputRequired()])
    date_of_birth = DateField("Date of birth", validators=[InputRequired(), AgeVerification(6)])
    address = StringField('Address', validators=[InputRequired()])
    native_city = StringField('Native city', validators=[InputRequired()])
    submit = SubmitField('Add student')
