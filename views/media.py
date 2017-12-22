from flask import request, jsonify

from logic.media import get_media, upsert_media


def media(username):
    """
    media accepts a POST request containing a medianame to add to the user specified by username
    media accepts a GET request and returns all the media associated with the user specified by username
    """
    if request.method == 'GET':
        return get_media(username)
    else:
        medianame = request.form['medianame']
        consumed = False

        # check if the consumed parameter was sent
        if 'consumed' in request.form:
            consumed = request.form['consumed']

        upsert_media(username, medianame, consumed)

        return jsonify(success=True)
