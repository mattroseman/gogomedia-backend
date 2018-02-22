from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from database import db

from routes import add_routes

login_manager = LoginManager()


def create_app(database_uri):
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    add_routes(app)

    db.init_app(app)
    db.create_all(app=app)

    login_manager.init_app(app)

    return app


if __name__ == '__main__':
    import configparser

    config = configparser.ConfigParser()
    config.read('alembic.ini')

    app = create_app(config['alembic']['sqlalchemy.url'])

    app.run()
