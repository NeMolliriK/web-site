from sqlalchemy import Column, Integer, String, Date, ForeignKey
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import relation


class Employee(SqlAlchemyBase, SerializerMixin):
    def set_date(self, date_of_birth):
        self.date_of_birth = date_of_birth
        self.age = relativedelta(date.today(), date_of_birth).years

    def update_age(self):
        self.age = relativedelta(date.today(), self.date_of_birth).years

    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    position = Column(String, nullable=False)
    speciality = Column(String, nullable=False)
    experience = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, ForeignKey("users.email"), unique=True, nullable=False, index=True)
    native_city = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    class_ = Column(String, unique=True)
    user = relation('User')
    pupils = relation("Student", back_populates='teacher')
