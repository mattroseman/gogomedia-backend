from flask import request, jsonify

from logic.user import add_user


def user():
    """
    user just accepts POST request containing a field with new user information
    """
    body = request.get_json()
    username = body['username']
    password = body['password']
    add_user(username, password)

    return jsonify(success=True)
