from database import db

from models.media import Media
from models.user import User


def add_media(username, medianame, consumed=False):
    """
    add_media creates a new media record with the given medianame and assigns the media to the user with the given
    username
    """
    userid = User.query.filter_by(username=username).first().id
    db.session.add(Media(medianame, userid))
    db.session.commit()


def update_media(username, medianame, consumed=False):
    """
    upadte_media updates an existing media record with he given medianame with the given values
    """
    media = Media.query.filter_by(medianame=medianame).first()
    media.consumed = consumed
    db.session.commit()


def get_media(username):
    """
    get_media returns all the media associated with the given username
    """
    return ',\n'.join(list(map(lambda media: str(media.medianame),
                               User.query.filter_by(username=username).first().media)))
