from database import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), unique=True, nullable=False)
    media = db.relationship('Media', backref='users', lazy=True)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User(id={}, username={})>'.format(self.id, self.username)
