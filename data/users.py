from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relation
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from datetime import date
from dateutil.relativedelta import relativedelta


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def set_date(self, date_of_birth):
        self.date_of_birth = date_of_birth
        self.age = relativedelta(date.today(), date_of_birth).years

    def update_age(self):
        self.age = relativedelta(date.today(), self.date_of_birth).years

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    employee = relation("Employee", back_populates='user', uselist=False)
    student = relation("Student", back_populates='user', uselist=False)
