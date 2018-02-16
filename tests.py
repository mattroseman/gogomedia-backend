import unittest
from flask_testing import TestCase

from app import create_app
from database import db

from models.user import User


class GoGoMediaTestCase(TestCase):

    def create_app(self):
        return create_app(config['alembic']['sqlalchemy.test.url'])

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status, '200 OK')

        self.assertEqual(response.get_data(), b'Hello World')

    def test_add_user(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user in db.session)


if __name__ == '__main__':
    import configparser

    config = configparser.ConfigParser()
    config.read('alembic.ini')

    unittest.main()
