from base_test_case import GoGoMediaBaseTestCase
from sqlalchemy.exc import StatementError

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
        self.assertEqual(media.medium, 'other')
        self.assertTrue(media in db.session)

    def test_add_consumed_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed=True)
        db.session.add(media)
        db.session.commit()

        self.assertTrue(media.consumed)

    def test_add_media_with_medium_type_film(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='film')
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medium, 'film')

    def test_add_media_with_medium_type_audio(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='audio')
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medium, 'audio')

    def test_add_media_with_medium_type_literature(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='literature')
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medium, 'literature')

    def test_add_media_with_medium_type_other(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='other')
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medium, 'other')

    def test_update_media_consumed(self):
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

    def test_update_media_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='literature')
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medium, 'literature')

        media.medium = 'audio'
        db.session.commit()

        self.assertEqual(media.medium, 'audio')

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

    def test_as_dict(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed=True, medium='literature')
        self.assertDictEqual(media.as_dict(), {
            'medianame': 'testmedianame',
            'consumed': True,
            'medium': 'literature'
        })
