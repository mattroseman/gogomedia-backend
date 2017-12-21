from database import db
from models.user import User


def add_user(username):
    """
    add_user takes a new user's information and adds it to the database
    @param username: a string representing the user's username
    """
    db.session.add(User(username))
    db.session.commit()
