from flask import request, jsonify

from logic.media import add_media, get_media, update_media
from models.media import Media


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
        if 'consumed' in request.form:
            consumed = request.form['consumed']

        if Media.query.filter_by(medianame=medianame).first():
            update_media(username, medianame, consumed)
        else:
            add_media(username, medianame, consumed)

        return jsonify(success=True)
