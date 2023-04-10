from controllers import ProfessorController, StudentController
from database import User


def register(user_id, username, role) -> User:
    new_user = None
    print(user_id, username, role)
    if role == "professor":
        new_user = ProfessorController.create(user_id, username)
    elif role == "student":
        new_user = StudentController.create(user_id, username)

    return new_user
