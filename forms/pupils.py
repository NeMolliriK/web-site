from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, DateField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, NumberRange
from validators import AgeVerification


class AddStudent(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('password_again')])
    password_again = PasswordField('Confirm password', validators=[InputRequired()])
    surname = StringField('Surname', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    patronymic = StringField('Patronymic', validators=[InputRequired()])
    date_of_birth = DateField("Date of birth", validators=[InputRequired(), AgeVerification(6)])
    class_number = IntegerField('Position', validators=[InputRequired(), NumberRange(min=1, max=11)])
    class_letter = StringField('Speciality', validators=[InputRequired(), Length(max=1)])
    address = StringField('Address', validators=[InputRequired()])
    native_city = StringField('Native city', validators=[InputRequired()])
    submit = SubmitField('Add an employee')


class EditStudent(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('password_again')])
    password_again = PasswordField('Confirm password', validators=[InputRequired()])
    surname = StringField('Surname', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    patronymic = StringField('Patronymic', validators=[InputRequired()])
    date_of_birth = DateField("Date of birth", validators=[InputRequired(), AgeVerification(6)])
    class_number = IntegerField('Position', validators=[InputRequired(), NumberRange(min=1, max=11)])
    class_letter = StringField('Speciality', validators=[InputRequired(), Length(max=1)])
    address = StringField('Address', validators=[InputRequired()])
    native_city = StringField('Native city', validators=[InputRequired()])
    submit = SubmitField('Edit worker')
