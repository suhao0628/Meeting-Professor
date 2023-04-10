from controllers import ProfessorController, StudentController,ActivityController
from database import User


def register(user_id, username, role) -> User:
    new_user = None
    print(user_id, username, role)
    if role == "professor":
        new_user = ProfessorController.create(user_id, username)
    elif role == "student":
        new_user = StudentController.create(user_id, username)

    return new_user


def get_all_activities() -> str:
    activities = ActivityController.get_all()
    if activities:
        message = "Available activities:\n\n"
        for activity in activities:
            joined_count = len(activity.participants)
            message += f"ID: {activity.activity_id}, Date: {activity.date}, Time: {activity.time}," \
                       f" Place: {activity.place}, Event: {activity.event}, Joined_Count: {joined_count}\n"
    else:
            message = "No activities found."
    return message


def get_activities_by_user(activities) -> str:
    if activities:
        message = "My activities:\n\n"
        for activity in activities:
            joined_count = len(activity.participants)
            message += f"ID: {activity.activity_id}, Date: {activity.date}, Time: {activity.time}," \
                       f" Place: {activity.place}, Event: {activity.event}, Joined_Count: {joined_count}\n\n"

            message += f"Participants: \n"
            for p in activity.participants:
                message += f"{p.user_name}\n"
            message += f"\n\n"
    else:
            message = "No joined activities found."
    return message

