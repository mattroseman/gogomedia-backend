import unittest
from flask_testing import TestCase

from app import create_app
from database import db

from models.user import User
from models.media import Media

from logic.user import add_user
from logic.media import add_media


class GoGoMediaTestCase(TestCase):

    def create_app(self):
        return create_app(config['alembic']['sqlalchemy.test.url'])

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class GoGoMediaModelTestCase(GoGoMediaTestCase):

    def test_add_user(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user in db.session)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, 'testname')

    def test_remove_user(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user in db.session)

        db.session.delete(user)
        db.session.commit()

        self.assertFalse(user in db.session)

    def test_add_media(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertFalse(media.consumed)
        self.assertTrue(media in db.session)

    def test_add_consumed_media(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed=True)
        db.session.add(media)
        db.session.commit()

        self.assertTrue(media.consumed)

    def test_update_media(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertFalse(media.consumed)

        media.consumed = True
        db.session.commit()

        self.assertTrue(media.consumed)

    def test_remove_media(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertTrue(media in db.session)

        db.session.delete(media)
        db.session.commit()

        self.assertFalse(media in db.session)


class GoGoMediaViewTestCase(GoGoMediaTestCase):

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status, '200 OK')

        self.assertEqual(response.get_data(), b'Hello World')


if __name__ == '__main__':
    import configparser

    config = configparser.ConfigParser()
    config.read('alembic.ini')

    unittest.main()
