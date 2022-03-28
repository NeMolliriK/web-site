from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, DateField, BooleanField, IntegerField
from wtforms.validators import InputRequired, EqualTo, NumberRange
from .validators import AgeVerification, RequiredIf, ClassCorrectness


class AddEmployee(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    password_again = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password')])
    surname = StringField('Surname', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    patronymic = StringField('Patronymic', validators=[InputRequired()])
    date_of_birth = DateField("Date of birth", validators=[InputRequired(), AgeVerification(16)])
    position = StringField('Position', validators=[InputRequired()])
    speciality = StringField('Speciality', validators=[InputRequired()])
    experience = IntegerField("Work experience", validators=[InputRequired(), NumberRange(0)])
    classroom_teacher = BooleanField("Classroom teacher")
    class_ = StringField('Class', validators=[ClassCorrectness(), RequiredIf("classroom_teacher")])
    address = StringField('Address', validators=[InputRequired()])
    native_city = StringField('Native city', validators=[InputRequired()])
    submit = SubmitField('Add employee')


class EditEmployee(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('password_again')])
    password_again = PasswordField('Confirm password', validators=[InputRequired()])
    surname = StringField('Surname', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    patronymic = StringField('Patronymic', validators=[InputRequired()])
    date_of_birth = DateField("Date of birth", validators=[InputRequired(), AgeVerification(16)])
    position = StringField('Position', validators=[InputRequired()])
    speciality = StringField('Speciality', validators=[InputRequired()])
    experience = IntegerField("Work experience", validators=[InputRequired(), NumberRange(0)])
    classroom_teacher = BooleanField("Classroom teacher")
    class_ = StringField('Class', validators=[ClassCorrectness(), RequiredIf("classroom_teacher")])
    address = StringField('Address', validators=[InputRequired()])
    native_city = StringField('Native city', validators=[InputRequired()])
    submit = SubmitField('Edit employee')
