from database import db

from models.media import Media
from models.user import User


def upsert_media(username, medianame, consumed=False):
    """
    upsert_media determines if a record with the given data already exists, and if so updates it,
    otherwise it inserts it as a new record
    """
    userid = User.query.filter_by(username=username).first().id

    # check if this media has been added for this user already
    if Media.query.filter((Media.medianame == medianame) & (Media.user == userid)).first():
        update_media(userid, medianame, consumed)
    else:
        add_media(userid, medianame, consumed)


def add_media(userid, medianame, consumed=False):
    """
    add_media creates a new media record with the given medianame and assigns the media to the user with the given
    username
    """
    db.session.add(Media(medianame, userid, consumed))
    db.session.commit()


def update_media(userid, medianame, consumed=False):
    """
    upadte_media updates an existing media record with he given medianame with the given values
    """
    media = Media.query.filter((Media.medianame == medianame) & (Media.user == userid)).first()
    media.consumed = consumed
    db.session.commit()


def get_media(username):
    """
    get_media returns all the media associated with the given username
    """
    return ',\n'.join(list(map(lambda media: str(media.medianame),
                               User.query.filter_by(username=username).first().media)))
