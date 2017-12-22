from database import db

from models.media import Media
from models.user import User


def add_media(username, medianame):
    """
    add_media creates a new media record with the given medianame and assigns the media to the user with the given
    username
    """
    userid = User.query.filter_by(username=username).first().id
    db.session.add(Media(medianame, userid))
    db.session.commit()
