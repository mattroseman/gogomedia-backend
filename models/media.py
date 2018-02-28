from database import db

medium_type = db.Enum('film', 'audio', 'literature', 'other', name='medium_type', validate_strings=True)


class Media(db.Model):
    __tablename__ = 'media'
    medianame = db.Column('medianame', db.String(80), primary_key=True)
    user = db.Column('user', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    consumed = db.Column('consumed', db.Boolean, default=False)
    medium = db.Column('medium', medium_type, default='other')

    def __init__(self, medianame, userid, consumed=False, medium='other'):
        self.medianame = medianame
        self.user = userid
        self.consumed = consumed
        self.medium = medium

    def __repr__(self):
        return '<Media(medianame={}, user={}, consumed={}, medium={})>'.format(
            self.medianame, self.user, self.consumed, self.medium)

    def as_dict(self):
        """
        returns a dict representing this media element. Used when returning media data as json in response
        """
        return {
            'medianame': self.medianame,
            'consumed': self.consumed,
            'medium': self.medium
        }
