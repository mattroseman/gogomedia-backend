from flask import request, jsonify

from logic.media import add_media, get_media


def media(username):
    """
    media accepts a POST request containing a medianame to add to the user specified by username
    media accepts a GET request and returns all the media associated with the user specified by username
    """
    if request.method == 'GET':
        return get_media(username)
    else:
        medianame = request.form['medianame']
        add_media(username, medianame)

        return jsonify(success=True)
