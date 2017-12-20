from gogomedia import db


class Users(db.Model):
    __tablename__ = 'media'
    id = db.Column('id', db.Integer, primary_key=True),
    medianame = db.Column('medianame', db.String(80), nullable=False),
    user = db.Column('user', db.Integer, db.ForeignKey('users.id'), nullable=False)
