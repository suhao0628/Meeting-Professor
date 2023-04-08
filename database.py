from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base,relationship

Base = declarative_base()

# Association table for many-to-many relationship between Student and Activity
student_activity_association = Table(
    'student_activity', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.user_id')),
    Column('activity_id', Integer, ForeignKey('activities.activity_id'))
)


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


class Activity(Base):
    __tablename__ = 'activities'
    activity_id = Column(Integer, primary_key=True)
    professor_id = Column(Integer, ForeignKey('professors.user_id'))
    date = Column(String)
    time = Column(String)
    place = Column(String)
    event = Column(String)
    participants = relationship("Student", secondary=student_activity_association, backref="activities")

    def __init__(self, professor_id, date, time, place, event):
        self.professor_id = professor_id
        self.date = date
        self.time = time
        self.place = place
        self.event = event
