from flask import request, jsonify
from flask_login import login_user, logout_user, current_user
from database import db

from logic.user import add_user, get_user


def register():
    """
    register accepts POST request containing a field with new user information
    """
    body = request.get_json()

    if 'username' not in body:
        return jsonify({
            'success': False,
            'message': 'Request body is missing the parameter \'username\''
        }), 422
    if 'password' not in body:
        return jsonify({
            'success': False,
            'message': 'Request body is missing the parameter \'password\''
        }), 422

    username = body['username']
    password = body['password']

    # If this user exists already
    if get_user(username):
        return jsonify({
            'success': False,
            'message': 'This username is already taken. Please choose another.'
        })

    user = add_user(username, password)

    auth_token = user.encode_auth_token()

    return jsonify({
        'success': True,
        'message': 'User was successfully registered',
        'auth_token': auth_token.decode()
    }), 201


def login():
    """
    login accepts a POST request containing username and password, it then validates this information
    and logs in the user
    """
    body = request.get_json()

    if 'username' not in body:
        return jsonify({
            'success': False,
            'message': 'Request body is missing the parameter \'username\''
        }), 422
    if 'password' not in body:
        return jsonify({
            'success': False,
            'message': 'Request body is missing the parameter \'password\''
        }), 422

    username = body['username']
    password = body['password']

    user = get_user(username)

    if user:
        if user.authenticate_password(password):
            user.authenticated = True
            db.session.commit()
            login_user(user, remember=True)

            auth_token = user.encode_auth_token()

            return jsonify({
                'success': True,
                'message': 'User successfully logged in.',
                'auth_token': auth_token.decode()
            })

    return jsonify({
        'success': False,
        'message': 'User doesn\'t exist. Please register user.'
    })


def logout():
    """
    logout logs the current user out
    """
    user = current_user
    user.authenticated = False
    db.session.commit()
    logout_user()

    return jsonify({
        'success': True,
        'message': 'User successfully logged out.'
    })
