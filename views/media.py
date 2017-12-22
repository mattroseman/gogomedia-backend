from flask import request, jsonify

from logic.media import get_media, upsert_media, remove_media


def media(username):
    """
    media accepts a POST request containing a medianame to add to the user specified by username
    media accepts a GET request and returns all the media associated with the user specified by username
    """
    if request.method == 'GET':
        if 'consumed' in request.args:
            if request.args.get('consumed') in ['True', 'true', 'T', 't', 'Yes', 'yes', 'Y', 'y']:
                return get_media(username, True)
            elif request.args.get('consumed') in ['False', 'false', 'F', 'f', 'No', 'no', 'N', 'n']:
                return get_media(username, False)
            else:
                # TODO return malformed parameters response
                pass
        else:
            return get_media(username)
    else:
        medianame = request.form['medianame']

        # if the remove parameter is in the request and set to True, remove this media item
        if 'remove' in request.form and request.form['remove']:
            remove_media(username, medianame)
            return jsonify(success=True)

        consumed = False
        # check if the consumed parameter was sent
        if 'consumed' in request.form:
            consumed = request.form['consumed']

        upsert_media(username, medianame, consumed)

        return jsonify(success=True)
