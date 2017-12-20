from gogomedia import db


class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column('id', db.Integer, primary_key=True),
    medianame = db.Column('medianame', db.String(80), nullable=False),
    user = db.Column('user', db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Media(id={}, medianame={}, user={})>'.format(self.id, self.medianame, self.user)
