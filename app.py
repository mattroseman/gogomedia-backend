from flask import Flask
from flask_cors import CORS
from database import db
from login_manager import login_manager
import configparser

from routes import add_routes


def create_app(test=False):
    app = Flask(__name__)
    CORS(app)

    # TODO user urandom to generate this
    app.secret_key = 'super secret key'

    config = configparser.ConfigParser()
    config.read('config.ini')

    database_uri = config['database']['sqlalchemy.test.url'] if test else config['database']['sqlalchemy.url']

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = test
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    add_routes(app)

    db.init_app(app)
    db.create_all(app=app)

    login_manager.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()

    app.run()
