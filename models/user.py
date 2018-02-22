from database import db
import bcrypt


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), unique=True, nullable=False)
    passhash = db.Column('passhash', db.String(60))
    passsalt = db.Column('passsalt', db.String(29))
    media = db.relationship('Media', backref='users', lazy=True)

    def __init__(self, username, password):
        self.username = username
        password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.passhash = bcrypt.hashpw(password, salt).decode('utf-8')
        self.passsalt = salt.decode('utf-8')

    def __repr__(self):
        return '<User(id={}, username={})>'.format(self.id, self.username)

    def get_id(self):
        return self.id
