from gogomedia import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<User(id={}, username={})>'.format(self.id, self.username)
