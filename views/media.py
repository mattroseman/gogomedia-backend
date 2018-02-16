from flask import request, jsonify

from logic.media import get_media, upsert_media, remove_media


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
            return jsonify(get_media(username))
    elif request.method == 'PUT':
        if 'name' not in body:
            # TODO return malformed parameters response if 'name' isn't present
            pass
        medianame = body['name']

        consumed = False
        if 'consumed' in body:
            consumed = body['consumed']

        upsert_media(username, medianame, consumed)

        return jsonify(success=True)
    else:
        if 'name' not in body:
            # TODO return malformed parameters response if 'name' isn't present
            pass
        medianame = body['name']

        remove_media(username, medianame)
        return jsonify(success=True)
