from sqlalchemy import Column, Integer, String, Date, ForeignKey
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import relation


class Student(SqlAlchemyBase, SerializerMixin):
    def set_date(self, date_of_birth):
        self.date_of_birth = date_of_birth
        self.age = relativedelta(date.today(), date_of_birth).years

    __tablename__ = 'pupils'
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    class_number = Column(Integer, nullable=False)
    class_letter = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    native_city = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    teacher_id = Column(Integer, ForeignKey("staff.id"), index=True)
    teacher = relation('Worker')
