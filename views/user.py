from flask import request, jsonify
from flask_login import login_user
from database import db

from logic.user import add_user, get_user


def user():
    """
    user just accepts POST request containing a field with new user information
    """
    body = request.get_json()
    username = body['username']
    password = body['password']
    add_user(username, password)

    return jsonify(success=True)


def login():
    """
    login accepts a POST request containing username and password, it then validates this information
    and logs in the user
    """
    body = request.get_json()
    username = body['username']
    password = body['password']
    user = get_user(username)

    if user:
        if user.authenticate_password(password):
            user.authenticated = True
            db.session.commit()
            login_user(user, remember=True)
            return jsonify(success=True)
    return jsonify(success=False)
