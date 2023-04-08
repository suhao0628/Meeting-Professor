from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_type = Column(String)  # 'professor' or 'student'
    __mapper_args__ = {
        'polymorphic_on': user_type
    }

    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name


class Professor(User):
    __tablename__ = 'professors'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'professor',
    }


class Student(User):
    __tablename__ = 'students'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

