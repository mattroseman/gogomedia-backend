from base_test_case import GoGoMediaBaseTestCase

from database import db

from models.user import User
from models.media import Media


class GoGoMediaMediaModelTestCase(GoGoMediaBaseTestCase):
    def test_add_media(self):
        user = User('testname', 'P@ssw0rd')
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
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed=True)
        db.session.add(media)
        db.session.commit()

        self.assertTrue(media.consumed)

    def test_update_media(self):
        user = User('testname', 'P@ssw0rd')
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
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertTrue(media in db.session)

        db.session.delete(media)
        db.session.commit()

        self.assertFalse(media in db.session)
