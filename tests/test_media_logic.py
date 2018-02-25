from base_test_case import GoGoMediaBaseTestCase

from database import db

from models.user import User
from models.media import Media

from logic.media import add_media, update_media, upsert_media, get_media, remove_media


class GoGoMediaMediaLogicTestCase(GoGoMediaBaseTestCase):
    def test_add_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        add_media(user.id, 'testmedianame')

        media = Media.query.filter((Media.medianame == 'testmedianame') & (Media.user == user.id)).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertFalse(media.consumed)

    def test_update_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertFalse(media.consumed)

        update_media(user.id, media.medianame, True)

        self.assertTrue(media.consumed)

        update_media(user.id, media.medianame, False)

        self.assertFalse(media.consumed)

    def test_upsert_media_with_new_element(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        upsert_media('testname', 'testmedianame')

        media = Media.query.filter((Media.medianame == 'testmedianame') & (Media.user == user.id)).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')

    def test_upsert_media_with_existing_element(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        upsert_media('testname', 'testmedianame', True)

        self.assertTrue(media.consumed)

        media_list = Media.query.filter(Media.user == user.id).all()

        self.assertEqual(media_list, [media])

    def test_remove_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertTrue(media in db.session)

        remove_media('testname', 'testmedianame')

        self.assertFalse(media in db.session)

    def test_get_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        media_list = sorted(get_media('testname'), key=lambda media: media['name'])

        self.assertEqual(media_list, [{'name': 'testmedianame', 'consumed': False}])

    def test_get_media_multiple_elements(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id)
        media2 = Media('testmedianame2', user.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.commit()

        media_list = sorted(get_media('testname'), key=lambda media: media['name'])

        self.assertEqual(media_list, [{'name': 'testmedianame1', 'consumed': False},
                                      {'name': 'testmedianame2', 'consumed': False}])

    def test_get_media_multiple_users(self):
        """
        'testname1': ['testmedianame1', 'testmedianame2', 'testmedianame3']
        'testname2': ['testmedianame4', 'testmedianame1']
        """
        user1 = User('testname1', 'P@ssw0rd')
        user2 = User('testname2', 'P@ssw0rd')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        media1 = Media('testmedianame1', user1.id)
        media2 = Media('testmedianame2', user1.id)
        media3 = Media('testmedianame3', user1.id)
        media4 = Media('testmedianame4', user2.id)
        media5 = Media('testmedianame1', user2.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.commit()

        user1_media_list = sorted(get_media('testname1'), key=lambda media: media['name'])

        self.assertEqual(user1_media_list, [{'name': 'testmedianame1', 'consumed': False},
                                            {'name': 'testmedianame2', 'consumed': False},
                                            {'name': 'testmedianame3', 'consumed': False}])

        user2_media_list = sorted(get_media('testname2'), key=lambda media: media['name'])

        self.assertEqual(user2_media_list, [{'name': 'testmedianame1', 'consumed': False},
                                            {'name': 'testmedianame4', 'consumed': False}])

    def test_get_meida_consumed_and_unconsumed(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed=True)
        media2 = Media('testmedianame2', user.id, consumed=True)
        media3 = Media('testmedianame3', user.id, consumed=False)
        media4 = Media('testmedianame4', user.id, consumed=False)
        media5 = Media('testmedianame5', user.id, consumed=True)
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.commit()

        consumed_media_list = sorted(get_media('testname', consumed=True), key=lambda media: media['name'])
        unconsumed_media_list = sorted(get_media('testname', consumed=False), key=lambda media: media['name'])

        self.assertEqual(consumed_media_list, [{'name': 'testmedianame1', 'consumed': True},
                                               {'name': 'testmedianame2', 'consumed': True},
                                               {'name': 'testmedianame5', 'consumed': True}])
        self.assertEqual(unconsumed_media_list, [{'name': 'testmedianame3', 'consumed': False},
                                                 {'name': 'testmedianame4', 'consumed': False}])

    def test_get_media_empty_list(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        empty_media_list = get_media('testname')
        empty_consumed_media_list = get_media('testname', consumed=True)
        empty_unconsumed_media_list = get_media('testname', consumed=False)

        self.assertEqual(empty_media_list, [])
        self.assertEqual(empty_consumed_media_list, [])
        self.assertEqual(empty_unconsumed_media_list, [])
