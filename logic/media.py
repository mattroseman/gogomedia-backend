from database import db

from models.media import Media
from models.user import User


def upsert_media(username, medianame, consumed=None, medium=None):
    """
    upsert_media determines if a record with the given data already exists, and if so updates it,
    otherwise it inserts it as a new record
    """
    userid = User.query.filter_by(username=username).first().id

    # check if this media has been added for this user already
    if Media.query.filter((Media.medianame == medianame) & (Media.user == userid)).first():
        return update_media(userid, medianame, consumed, medium)
    else:
        # If consumed wasn't specified, use False
        # If medium wasn't specified, use 'other'
        return add_media(userid,
                         medianame,
                         consumed if consumed is not None else False,
                         medium if medium is not None else 'other')


def add_media(userid, medianame, consumed=False, medium='other'):
    """
    add_media creates a new media record with the given medianame and assigns the media to the user with the given
    username
    """
    media = Media(medianame, userid, consumed, medium)
    db.session.add(media)
    db.session.commit()

    return media


def update_media(userid, medianame, consumed=None, medium=None):
    """
    upadte_media updates an existing media record with he given medianame with the given values
    @param consumed: If this parameter is missing or set to None, no change is made to the consumed property
    @param medium: If this parameter is missing or set to None, no change is made to the medium property
    """
    media = Media.query.filter((Media.medianame == medianame) & (Media.user == userid)).first()
    if consumed is not None:
        media.consumed = consumed
    if medium is not None:
        media.medium = medium
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


def get_media(username, consumed=None, medium=None):
    """
    get_media returns all the media associated with the given username. If consumed is True or False,
    then only the media with the same consumed state will be returned. If medium is set to a medium type,
    then only the media with the same medium type will be returned.
    @return: a list of media elements
    """
    media_list = User.query.filter_by(username=username).first().media

    # if consumed is set then only return the media items that have the same consumed value
    if consumed is not None:
        media_list = [media for media in media_list if media.consumed == consumed]

    # if medium is set then only return the media items that have the same medium type
    if medium is not None:
        media_list = [media for media in media_list if media.medium == medium]

    return media_list
