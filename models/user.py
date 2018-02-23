from database import db
import bcrypt


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), unique=True, nullable=False)
    passhash = db.Column('passhash', db.String(60))
    authenticated = db.Column('authenticated', db.Boolean, default=False)
    media = db.relationship('Media', backref='users', lazy=True)

    def __init__(self, username, password):
        self.username = username
        password = password.encode('utf-8')
        self.passhash = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    def __repr__(self):
        return '<User(id={}, username={}, passhash={}, authenticated={})>'.format(
            self.id, self.username, self.passhash, self.authenticated)

    def get_id(self):
        """
        get_id returns the unique id of this user as a unicode string
        """
        return str(self.id)
        # return str(self.id).encode('utf-8').decode('utf-8')

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        # Currently there is no mechanism for "deactivating" accounts
        # if there was the code would be here
        return True

    def is_anonymous(self):
        # Currently there is no mechanism for "anonymous" users
        return False

    def authenticate_password(self, password):
        """
        authenticate_password takes an unhashed password, and returns True if this mathces the
        hashed password + salt for this user
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.passhash.encode('utf-8'))
