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
