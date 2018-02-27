from flask import request, jsonify, current_app

from logic.media import get_media, upsert_media, remove_media
from logic.user import get_user
from logic.login import login_required


@login_required
def media(logged_in_user, username):
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

    # This user is the one specified in url parameters, must match the auth token user
    user = get_user(username)
    if user is None:
        # there is no user with this name, return incorrect parameters response
        return jsonify({
            'success': False,
            'message': 'user doesn\'t exist'
        }), 422

    if logged_in_user != user and not current_app.config['LOGIN_DISABLED']:
        # you can't get media for a user you are not logged in as
        return jsonify({
            'success': False,
            'message': 'not logged in as this user'
        }), 401

    if request.method == 'GET':
        if 'consumed' in request.args:
            if request.args.get('consumed') in ['True', 'true', 'T', 't', 'Yes', 'yes', 'Y', 'y']:
                return jsonify({
                    'success': True,
                    'message': 'successfully got all consumed media for the logged in user',
                    'data': get_media(username, consumed=True)
                })
            elif request.args.get('consumed') in ['False', 'false', 'F', 'f', 'No', 'no', 'N', 'n']:
                return jsonify({
                    'success': True,
                    'message': 'successfully got all unconsumed media for the logged in user',
                    'data': get_media(username, consumed=False)
                })
            else:
                # return malformed parameters response
                return jsonify({
                    'success': False,
                    'message': 'consumed url parameter must be \'yes\' or \'no\''
                }), 422
        else:
            return jsonify({
                'success': True,
                'message': 'successfully got all media for the logged in user',
                'data': get_media(username)
            })

    elif request.method == 'PUT':
        if 'name' not in body:
            # return malformed parameters response if 'name' isn't present
            return jsonify({
                'success': False,
                'message': 'missing parameter \'name\''
            }), 422

        medianame = body['name']

        consumed = False
        if 'consumed' in body:
            consumed = body['consumed']

        upsert_media(username, medianame, consumed)

        # TODO possibly have upsert_media return the media element, and simply put that in the return parameter 'data'
        return jsonify({
            'success': True,
            'message': 'successfully added/updated media element',
            'data': {'name': medianame, 'consumed': consumed}
        })
    else:  # request.method == 'DELETE'
        if 'name' not in body:
            # return malformed parameters response if 'name' isn't present
            return jsonify({
                'success': False,
                'message': 'missing parameter \'name\''
            }), 422

        medianame = body['name']

        media = remove_media(username, medianame)
        return jsonify({
            'success': True,
            'message': 'successfully deleted media element'
        })
