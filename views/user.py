from flask import request, jsonify

from logic.user import add_user


def user():
    """
    user just accepts POST request containing a field with new user information
    """
    username = request.form['username']
    add_user(username)

    return jsonify(success=True)
