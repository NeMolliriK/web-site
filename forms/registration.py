from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, DateField
from wtforms.validators import InputRequired, EqualTo
from validators import AgeVerification


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('password_again')])
    password_again = PasswordField('Confirm password', validators=[InputRequired()])
    surname = StringField('Surname', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    patronymic = StringField('Patronymic', validators=[InputRequired()])
    date_of_birth = DateField("Date of birth", validators=[InputRequired(), AgeVerification(14)])
    submit = SubmitField('Register')
