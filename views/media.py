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
            'medium': a string indicating the type of this media
                represents an Enum of possible values ('film', 'audio', 'literature', 'other')
        }

    media accepts a GET request and returns all the media associated with the user specified by username
        a request arg 'consumed' can be set to yes or no, and only consumed or unconsumed media will be returned
        a request arg 'medium' can be set to 'film', 'audio', 'literature', or 'other' and only media with the same
            medium will be returned
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
        # Check if url parameters have acceptible values
        if 'consumed' in request.args and request.args.get('consumed') not in ['yes', 'no']:
            return jsonify({
                'success': False,
                'message': 'consumed url parameter must be \'yes\' or \'no\''
            }), 422

        if 'medium' in request.args and request.args.get('medium') not in ['film', 'audio', 'literature', 'other']:
            return jsonify({
                'success': False,
                'message': 'medium url parameter must be \'film\', \'audio\', \'literature\', or \'other\''
            }), 422

        media_list = get_media(username,
                               request.args.get('consumed') == 'yes' if 'consumed' in request.args else None,
                               request.args.get('medium') if 'medium' in request.args else None)

        return jsonify({
            'success': True,
            'message': 'successfully got media for logged in user',
            'data': list(map(lambda media: media.as_dict(), media_list))
        })
    elif request.method == 'PUT':
        if 'name' not in body:
            # return malformed parameters response if 'name' isn't present
            return jsonify({
                'success': False,
                'message': 'missing parameter \'name\''
            }), 422

        medianame = body['name']

        consumed = None
        if 'consumed' in body:
            consumed = body['consumed']

        medium = None
        if 'medium' in body:
            medium = body['medium']

        media = upsert_media(username, medianame, consumed, medium)

        return jsonify({
            'success': True,
            'message': 'successfully added/updated media element',
            'data': media.as_dict()
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
