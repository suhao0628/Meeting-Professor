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

    @staticmethod
    def get_all():
        return session.query(Activity).all()

    @staticmethod
    def add_student(activity_id, student_id):
        activity = session.query(Activity).filter_by(activity_id=activity_id).first()
        student = session.query(Student).filter_by(user_id=student_id).first()
        if activity and student:
            activity.participants.append(student)
            session.commit()
            return True
        return False

    @staticmethod
    def is_student_in_activity(activity_id, student_id):
        student = session.query(Student).filter_by(user_id=student_id).first()
        joined_activities = [int(a.activity_id) for a in student.activities]
        if int(activity_id) in joined_activities:
            return True
        return False

    @staticmethod
    def get_activities_by_professor_id(professor_id):
        activities = session.query(Activity).filter_by(professor_id=professor_id).all()
        return activities


    @staticmethod
    def delete_user_from_activity(student_id, activity_id):
        activity = session.query(Activity).filter_by(activity_id=activity_id).first()
        student = session.query(Student).filter_by(user_id=student_id).first()
        try:
            student.activities.remove(activity)
            session.commit()
            return True
        except:
            return False

