from database import db


class Media(db.Model):
    __tablename__ = 'media'
    medianame = db.Column('medianame', db.String(80), primary_key=True)
    user = db.Column('user', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    consumed = db.Column('consumed', db.Boolean, default=False)

    def __init__(self, medianame, userid, consumed=False):
        self.medianame = medianame
        self.user = userid
        self.consumed = consumed

    def __repr__(self):
        return '<Media(medianame={}, user={}, consumed={})>'.format(self.medianame, self.user, self.consumed)
