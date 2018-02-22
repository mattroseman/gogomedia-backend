from database import db
from models.user import User
import bcrypt


def add_user(username, password):
    """
    add_user takes a new user's information and adds it to the database
    @param username: a string representing the user's username
    @param password: a string representing the user's password
    """
    db.session.add(User(username, password))
    db.session.commit()


def get_user(username):
    """
    get_user queries the database for a user with the given username, returning the user instance
    """
    return User.query.filter_by(username=username).first()
