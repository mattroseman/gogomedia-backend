from database import db


class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    medianame = db.Column(db.String(80), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    consumed = db.Column(db.Boolean, default=False)

    def __init__(self, medianame, userid, consumed=False):
        self.medianame = medianame
        self.user = userid
        self.consumed = consumed

    def __repr__(self):
        return '<Media(id={}, medianame={}, user={})>'.format(self.id, self.medianame, self.user)
