from database import db

from models.media import Media
from models.user import User


def upsert_media(username, medianame, medium=None, consumed_state=None):
    """
    upsert_media determines if a record with the given data already exists, and if so updates it,
    otherwise it inserts it as a new record
    """
    userid = User.query.filter_by(username=username).first().id

    # check if this media has been added for this user already
    if Media.query.filter((Media.medianame == medianame) & (Media.user == userid)).first():
        return update_media(userid, medianame, medium, consumed_state)
    else:
        # If consumed wasn't specified, use False
        # If medium wasn't specified, use 'other'
        return add_media(userid,
                         medianame,
                         medium if medium is not None else 'other',
                         consumed_state if consumed_state is not None else 'not started')


def add_media(userid, medianame, medium='other', consumed_state='not started'):
    """
    add_media creates a new media record with the given medianame and assigns the media to the user with the given
    username
    """
    media = Media(medianame, userid, medium, consumed_state)
    db.session.add(media)
    db.session.commit()

    return media


def update_media(userid, medianame, medium=None, consumed_state=None):
    """
    upadte_media updates an existing media record with he given medianame with the given values
    @param medium: If this parameter is missing or set to None, no change is made to the medium property
    @param consumed_state: If this parameter is missing or set to None, no change is made to the consumed_state property
    """
    media = Media.query.filter((Media.medianame == medianame) & (Media.user == userid)).first()
    if consumed_state is not None:
        media.consumed_state = consumed_state
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


def get_media(username, medium=None, consumed_state=None):
    """
    get_media returns all the media associated with the given username.
    If medium is set to a medium type, then only the media with the same medium type will be returned.
    If consumed_state is set to a consumed_state, then only the media with the same consumed_state will be returned.
    @return: a list of media elements
    """
    media_list = User.query.filter_by(username=username).first().media

    # if medium is set then only return the media items that have the same medium type
    if medium is not None:
        media_list = [media for media in media_list if media.medium == medium]

    # if consumed is set then only return the media items that have the same consumed value
    if consumed_state is not None:
        media_list = [media for media in media_list if media.consumed_state == consumed_state]

    return media_list
