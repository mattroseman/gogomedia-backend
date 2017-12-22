from flask_testing import TestCase
import configparser
import unittest

from app import create_app
from database import db

config = configparser.ConfigParser()
config.read('alembic.ini')


class GogomediaTestCase(TestCase):

    SQLALCHEMY_DATABASE_URI = config['alembic']['sqlalchemy.test.url']
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        # db.create_all()
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        response = self.client.get('/')
        assert 'Hello World' == response


if __name__ == '__main__':
    unittest.main()
