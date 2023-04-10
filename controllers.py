from database import User, Professor, Student, Activity,session


class UserController:

    @staticmethod
    def get(user_id):
        return session.query(User).get(user_id)


class ProfessorController:

    @staticmethod
    def create(user_id, user_name):
        professor = Professor(user_id=user_id, user_name=user_name)
        session.add(professor)
        session.commit()
        return professor

    @staticmethod
    def get(user_id):
        return session.query(Professor).get(user_id)

    @staticmethod
    def update(user_id, user_name):
        professor = session.query(Professor).get(user_id)
        if professor:
            professor.user_name = user_name
            session.commit()

    @staticmethod
    def delete(user_id):
        professor = session.query(Professor).get(user_id)
        if professor:
            session.delete(professor)
            session.commit()


class StudentController:

    @staticmethod
    def create(user_id, user_name):
        student = Student(user_id=user_id, user_name=user_name)
        session.add(student)
        session.commit()
        return student

    @staticmethod
    def get(user_id):
        return session.query(Student).get(user_id)

    @staticmethod
    def update(user_id, user_name):
        student = session.query(Student).get(user_id)
        if student:
            student.user_name = user_name
            session.commit()

    @staticmethod
    def delete(user_id):
        student = session.query(Student).get(user_id)
        if student:
            session.delete(student)
            session.commit()


class ActivityController:

    @staticmethod
    def create(professor_id, date, time, place, event):
        activity = Activity(professor_id=professor_id, date=date, time=time, place=place, event=event)
        session.add(activity)
        session.commit()
        return activity

    @staticmethod
    def get(activity_id):
        return session.query(Activity).get(activity_id)

    @staticmethod
    def update(activity_id, date=None, time=None, place=None, event=None):
        activity = session.query(Activity).get(activity_id)
        if activity:
            if date:
                activity.date = date
            if time:
                activity.time = time
            if place:
                activity.place = place
            if event:
                activity.event = event
            session.commit()

    @staticmethod
    def delete(activity_id):
        activity = session.query(Activity).get(activity_id)
        if activity:
            session.delete(activity)
            session.commit()
