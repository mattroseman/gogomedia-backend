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
        return update_media(userid, medianame, consumed)
    else:
        return add_media(userid, medianame, consumed)


def add_media(userid, medianame, consumed=False):
    """
    add_media creates a new media record with the given medianame and assigns the media to the user with the given
    username
    """
    media = Media(medianame, userid, consumed)
    db.session.add(media)
    db.session.commit()

    return media


def update_media(userid, medianame, consumed):
    """
    upadte_media updates an existing media record with he given medianame with the given values
    """
    media = Media.query.filter((Media.medianame == medianame) & (Media.user == userid)).first()
    media.consumed = consumed
    db.session.commit()

    return media


def remove_media(username, medianame):
    """
    remove_media removes a Media record from the database
    """
    userid = User.query.filter_by(username=username).first().id
    # if there is no record for this medianame for this user, then filter returns nothing, and nothing is deleted
    Media.query.filter((Media.medianame == medianame) & (Media.user == userid)).delete()
    db.session.commit()


def get_media(username, consumed=None):
    """
    get_media returns all the media associated with the given username. If consumed is True or False,
    then only the media with the same consumed state will be returned
    @return: a set of strings indicating media names belonging to the given username
    """
    media_list = User.query.filter_by(username=username).first().media

    # if consumed is set then only return the media items that have the same consumed value
    if consumed is not None:
        media_list = filter(lambda media: media.consumed == consumed, media_list)

    # modify the key's for each media item
    return set(map(lambda media: media.medianame, media_list))
