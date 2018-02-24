from flask import request, jsonify, current_app
from flask_login import login_required, current_user

from logic.media import get_media, upsert_media, remove_media
from logic.user import get_user


@login_required
def media(username):
    """
    media accepts a PUT request with formdata that matches
        {
            'name': a string representing the name of the media to insert/update
            'consumed': a boolean indicating if this media has been consumed or not
                if consumed isn't present, it defaults to False
        }

    media accepts a GET request and returns all the media associated with the user specified by username
        a request arg 'consumed' can be set to yes or no, and only consumed or unconsumed media will be returned
        if no request arg is present, all media will be returned

    media accepts a DELETE request with formdata that matches
        {
            'name': a string representing the name of the media to delete
        }
    """
    body = request.get_json()
    user = get_user(username)
    if user is None:
        # there is no user with this name, return incorrect parameters response
        return jsonify({
            'success': False,
            'message': 'User doesn\'t exist. Please register user.'
        })

    if current_user != user and not current_app.config['LOGIN_DISABLED']:
        # you can't get media for a user you are not logged in as
        return jsonify({
            'success': False,
            'message': 'You are not logged in as this user. Please log in.'
        })

    if request.method == 'GET':
        if 'consumed' in request.args:
            if request.args.get('consumed') in ['True', 'true', 'T', 't', 'Yes', 'yes', 'Y', 'y']:
                return jsonify({
                    'success': True,
                    'message': 'Successfully got a list of all consumed media for the logged in user.',
                    'data': get_media(username, consumed=True)
                })
            elif request.args.get('consumed') in ['False', 'false', 'F', 'f', 'No', 'no', 'N', 'n']:
                return jsonify({
                    'success': True,
                    'message': 'Successfully got a list of all unconsumed media for the logged in user.',
                    'data': get_media(username, consumed=False)
                })
            else:
                # return malformed parameters response
                return jsonify({
                    'success': False,
                    'message': 'Some of the URL parameters where malformed.'
                })
        else:
            return jsonify({
                'success': True,
                'message': 'Successfully got a list of all media for the logged in user.',
                'data': get_media(username)
            })

    elif request.method == 'PUT':
        if 'name' not in body:
            # return malformed parameters response if 'name' isn't present
            return jsonify({
                'success': False,
                'message': 'Request body is missing the parameter \'name\'.'
            }), 422

        medianame = body['name']

        consumed = False
        if 'consumed' in body:
            consumed = body['consumed']

        upsert_media(username, medianame, consumed)

        # TODO possibly have upsert_media return the media element, and simply put that in the return parameter 'data'
        return jsonify({
            'success': True,
            'message': 'Successfully added/updated media element.',
            'data': {'name': medianame, 'consumed': consumed}
        })
    else:  # request.method == 'DELETE'
        if 'name' not in body:
            # return malformed parameters response if 'name' isn't present
            return jsonify({
                'success': False,
                'message': 'Request body is missing the parameter \'name\'.'
            }), 422

        medianame = body['name']

        media = remove_media(username, medianame)
        return jsonify({
            'success': True,
            'message': 'Successfully deleted media element.'
        })
