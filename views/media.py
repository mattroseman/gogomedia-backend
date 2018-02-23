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
        # TODO there is no user with this name, return incorrect parameters response
        return jsonify({'success': False})

    if current_user != user and not current_app.config['LOGIN_DISABLED']:
        # TODO you can't get media for a user you are not logged in as
        return jsonify({'success': False})

    if request.method == 'GET':
        if 'consumed' in request.args:
            if request.args.get('consumed') in ['True', 'true', 'T', 't', 'Yes', 'yes', 'Y', 'y']:
                return jsonify(get_media(username, consumed=True))
            elif request.args.get('consumed') in ['False', 'false', 'F', 'f', 'No', 'no', 'N', 'n']:
                return jsonify(get_media(username, consumed=False))
            else:
                # TODO return malformed parameters response
                pass
        else:
            return jsonify(list(get_media(username)))
    elif request.method == 'PUT':
        if 'name' not in body:
            # TODO return malformed parameters response if 'name' isn't present
            pass
        medianame = body['name']

        consumed = False
        if 'consumed' in body:
            consumed = body['consumed']

        upsert_media(username, medianame, consumed)

        return jsonify({'name': medianame, 'consumed': consumed})
    else:  # request.method == 'DELETE'
        if 'name' not in body:
            # TODO return malformed parameters response if 'name' isn't present
            pass
        medianame = body['name']

        media = remove_media(username, medianame)
        return jsonify({'success': True})
