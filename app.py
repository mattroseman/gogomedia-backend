import os
from flask import Flask
from flask_cors import CORS
from database import db
import configparser

from routes import add_routes


def create_app(test=False):
    app = Flask(__name__)
    CORS(app)

    # TODO user urandom to generate this
    app.secret_key = 'super secret key'

    config = configparser.ConfigParser()
    config.read('config.ini')
    if test:
        if os.environ.get('TEST_DATABASE_URL') is None:
            database_uri = config['database']['sqlalchemy.test.url']
        else:
            database_uri = os.environ.get('TEST_DATABASE_URL')
    else:
        if os.environ.get('DATABASE_URL') is None:
            database_uri = config['database']['sqlalchemy.url']
        else:
            database_uri = os.environ.get('DATABASE_URL')

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = test
    app.config['LOGIN_DISABLED'] = test
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    add_routes(app)

    db.init_app(app)
    db.create_all(app=app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
