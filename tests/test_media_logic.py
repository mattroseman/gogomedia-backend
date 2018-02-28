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

        media = add_media(user.id, 'testmedianame')

        self.assertIsNotNone(media)
        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertFalse(media.consumed)
        self.assertEqual(media.medium, 'other')

    def test_add_media_with_consumed_argument(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = add_media(user.id, 'testmedianame', consumed=True)

        self.assertIsNotNone(media)
        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertTrue(media.consumed)
        self.assertEqual(media.medium, 'other')

    def test_add_media_with_medium_argument(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = add_media(user.id, 'testmedianame', medium='audio')

        self.assertIsNotNone(media)
        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertFalse(media.consumed)
        self.assertEqual(media.medium, 'audio')

    def test_update_media_consumed_property(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertFalse(media.consumed)
        self.assertEqual(media.medium, 'other')

        returned_media = update_media(user.id, media.medianame, consumed=True)

        self.assertEqual(returned_media, media)
        self.assertTrue(media.consumed)
        self.assertEqual(media.medium, 'other')

        returned_media = update_media(user.id, media.medianame, consumed=False)

        self.assertEqual(returned_media, media)
        self.assertFalse(media.consumed)
        self.assertEqual(media.medium, 'other')

    def test_update_media_medium_property(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertEqual(media.medium, 'other')

        returned_media = update_media(user.id, media.medianame, medium='film')

        self.assertEqual(returned_media, media)
        self.assertFalse(media.consumed)
        self.assertEqual(media.medium, 'film')

        returned_media = update_media(user.id, media.medianame, medium='audio')

        self.assertEqual(returned_media, media)
        self.assertFalse(media.consumed)
        self.assertEqual(media.medium, 'audio')

    def test_update_media_no_change(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed=True, medium='film')
        db.session.add(media)
        db.session.commit()

        returned_media = update_media(user.id, media.medianame)

        self.assertEqual(returned_media, media)
        self.assertTrue(media.consumed)
        self.assertEqual(media.medium, 'film')

    def test_upsert_media_with_new_element(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = upsert_media('testname', 'testmedianame')

        self.assertIsNotNone(media)
        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertFalse(media.consumed)
        self.assertEqual(media.medium, 'other')

    def test_upsert_media_with_new_element_consumed_property_set(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = upsert_media('testname', 'testmedianame', consumed=True)

        self.assertIsNotNone(media)
        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertTrue(media.consumed)
        self.assertEqual(media.medium, 'other')

    def test_upsert_media_with_new_element_medium_property_set(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = upsert_media('testname', 'testmedianame', medium='literature')

        self.assertIsNotNone(media)
        self.assertIn(media, db.session)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertFalse(media.consumed)
        self.assertEqual(media.medium, 'literature')

    def test_upsert_media_with_existing_element(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        returned_media = upsert_media('testname', 'testmedianame', consumed=True)

        self.assertIsNotNone(returned_media)
        self.assertEqual(returned_media, media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertTrue(media.consumed)
        self.assertEqual(media.medium, 'other')

        media_list = Media.query.filter(Media.user == user.id).all()

        self.assertListEqual(media_list, [media])

    def test_upsert_media_with_existing_element_update_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, medium='film')
        db.session.add(media)
        db.session.commit()

        returned_media = upsert_media('testname', 'testmedianame', medium='audio')

        self.assertIsNotNone(returned_media)
        self.assertEqual(returned_media, media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertFalse(media.consumed)
        self.assertEqual(media.medium, 'audio')

        media_list = Media.query.filter(Media.user == user.id).all()

        self.assertListEqual(media_list, [media])

    def test_upsert_media_with_existing_element_no_change(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed=True, medium='audio')
        db.session.add(media)
        db.session.commit()

        returned_media = upsert_media('testname', 'testmedianame')

        self.assertIsNotNone(returned_media)
        self.assertEqual(returned_media, media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertTrue(media.consumed)
        self.assertEqual(media.medium, 'audio')

        media_list = Media.query.filter(Media.user == user.id).all()

        self.assertListEqual(media_list, [media])

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

        media_list = sorted(get_media('testname'), key=lambda media: media.medianame)

        self.assertEqual(media_list, [media])

    def test_get_media_multiple_elements(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id)
        media2 = Media('testmedianame2', user.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.commit()

        media_list = sorted(get_media('testname'), key=lambda media: media.medianame)

        self.assertListEqual(media_list, [media1, media2])

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

        user1_media_list = sorted(get_media('testname1'), key=lambda media: media.medianame)

        self.assertListEqual(user1_media_list, [media1, media2, media3])

        user2_media_list = sorted(get_media('testname2'), key=lambda media: media.medianame)

        self.assertListEqual(user2_media_list, [media5, media4])

    def test_get_media_consumed_and_unconsumed(self):
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

        consumed_media_list = sorted(get_media('testname', consumed=True), key=lambda media: media.medianame)
        unconsumed_media_list = sorted(get_media('testname', consumed=False), key=lambda media: media.medianame)

        self.assertListEqual(consumed_media_list, [media1, media2, media5])
        self.assertListEqual(unconsumed_media_list, [media3, media4])

    def test_get_media_with_specific_medium(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id, consumed=True, medium='other')
        media2 = Media('testmedianame2', user.id, medium='film')
        media3 = Media('testmedianame3', user.id, consumed=False, medium='literature')
        media4 = Media('testmedianame4', user.id, consumed=False, medium='audio')
        media5 = Media('testmedianame5', user.id, consumed=True, medium='film')
        media6 = Media('testmedianame6', user.id, consumed=False, medium='film')
        media7 = Media('testmedianame7', user.id, medium='audio')
        db.session.add(media1)
        db.session.add(media2)
        db.session.add(media3)
        db.session.add(media4)
        db.session.add(media5)
        db.session.add(media6)
        db.session.add(media7)
        db.session.commit()

        other_media_list = sorted(get_media('testname', medium='other'), key=lambda media: media.medianame)
        film_media_list = sorted(get_media('testname', medium='film'), key=lambda media: media.medianame)
        audio_media_list = sorted(get_media('testname', medium='audio'), key=lambda media: media.medianame)
        literature_media_list = sorted(get_media('testname', medium='literature'), key=lambda media: media.medianame)

        self.assertListEqual(other_media_list, [media1])
        self.assertListEqual(film_media_list, [media2, media5, media6])
        self.assertListEqual(audio_media_list, [media4, media7])
        self.assertListEqual(literature_media_list, [media3])

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
