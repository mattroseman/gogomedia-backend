from flask import request, jsonify

from logic.media import add_media


def media(username):
    """
    media accepts a POST request containing a medianame to add to the user specified by username
    """
    medianame = request.form['medianame']
    add_media(username, medianame)

    return jsonify(success=True)
