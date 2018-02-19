import unittest
from flask_testing import TestCase
import json

from app import create_app
from database import db

from models.user import User
from models.media import Media

from logic.user import add_user
from logic.media import upsert_media
from logic.media import add_media
from logic.media import update_media
from logic.media import remove_media
from logic.media import get_media


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


class GoGoMediaLogicTestCase(GoGoMediaTestCase):

    def test_add_user(self):
        add_user('testname')

        user = User.query.filter(User.username == 'testname').first()

        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testname')

    def test_add_media(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        add_media(user.id, 'testmedianame')

        media = Media.query.filter((Media.medianame == 'testmedianame') & (Media.user == user.id)).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertFalse(media.consumed)

    def test_update_media(self):
        user = User('testname')
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
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        upsert_media('testname', 'testmedianame')

        media = Media.query.filter((Media.medianame == 'testmedianame') & (Media.user == user.id)).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')

    def test_upsert_media_with_existing_element(self):
        user = User('testname')
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
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        self.assertTrue(media in db.session)

        remove_media('testname', 'testmedianame')

        self.assertFalse(media in db.session)

    def test_get_media(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        media_list = get_media('testname')

        self.assertEqual(media_list, {'testmedianame'})

    def test_get_media_multiple_elements(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id)
        media2 = Media('testmedianame2', user.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.commit()

        media_list = get_media('testname')

        self.assertEqual(media_list, {'testmedianame1', 'testmedianame2'})

    def test_get_media_multiple_users(self):
        """
        'testname1': ['testmedianame1', 'testmedianame2', 'testmedianame3']
        'testname2': ['testmedianame4', 'testmedianame1']
        """
        user1 = User('testname1')
        user2 = User('testname2')
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

        user1_media_list = get_media('testname1')

        self.assertEqual(user1_media_list, {'testmedianame1', 'testmedianame2', 'testmedianame3'})

        user2_media_list = get_media('testname2')

        self.assertEqual(user2_media_list, {'testmedianame4', 'testmedianame1'})

    def test_get_meida_consumed_and_unconsumed(self):
        user = User('testname')
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

        consumed_media_list = get_media('testname', consumed=True)
        unconsumed_media_list = get_media('testname', consumed=False)

        self.assertEqual(consumed_media_list, {'testmedianame1', 'testmedianame2', 'testmedianame5'})
        self.assertEqual(unconsumed_media_list, {'testmedianame3', 'testmedianame4'})

    def test_get_media_empty_set(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        empty_media_list = get_media('testname')
        empty_consumed_media_list = get_media('testname', consumed=True)
        empty_unconsumed_media_list = get_media('testname', consumed=False)

        self.assertEqual(empty_media_list, set())
        self.assertEqual(empty_consumed_media_list, set())
        self.assertEqual(empty_unconsumed_media_list, set())


class GoGoMediaViewTestCase(GoGoMediaTestCase):

    def test_index(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'Hello World')

    def test_user(self):
        response = self.client.post('/user',
                                    data=json.dumps({'username': 'testname'}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'success': True})

        user = User.query.filter(User.username == 'testname').first()

        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testname')

    def test_add_media(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'name': 'testmedianame', 'consumed': False})

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertFalse(media.consumed)

    def test_add_media_consumed(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed': True}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'name': 'testmedianame', 'consumed': True})

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertTrue(media.consumed)

    def test_add_media_unconsumed(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed': False}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'name': 'testmedianame', 'consumed': False})

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertFalse(media.consumed)

    def test_update_media(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed=False)
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed': True}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'name': 'testmedianame', 'consumed': True})

        media_list = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertTrue(media_list[0].consumed)

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed': False}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'name': 'testmedianame', 'consumed': False})

        media_list = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertFalse(media_list[0].consumed)

    def test_get_media(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id)
        media2 = Media('testmedianame2', user.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.commit()

        response = self.client.get('/user/testname/media')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(json.loads(response.get_data(as_text=True))), {'testmedianame1', 'testmedianame2'})

    def test_get_consumed_media(self):
        user = User('testname')
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

        response = self.client.get('/user/testname/media?consumed=yes')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(json.loads(response.get_data(as_text=True))),
                         {'testmedianame1', 'testmedianame2', 'testmedianame5'})

    def test_get_unconsumed_media(self):
        user = User('testname')
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

        response = self.client.get('/user/testname/media?consumed=no')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(json.loads(response.get_data(as_text=True))),
                         {'testmedianame3', 'testmedianame4'})

    def test_delete_media(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.delete('/user/testname/media',
                                      data=json.dumps({'name': 'testmedianame'}),
                                      content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'success': True})

        media_list = Media.query.filter(Media.user == user.id).all()

        self.assertEqual(media_list, [])

    def test_delete_unexisting_media(self):
        user = User('testname')
        db.session.add(user)
        db.session.commit()

        response = self.client.delete('/user/testname/media',
                                      data=json.dumps({'name': 'testmedianame'}),
                                      content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.get_data(as_text=True)), {'success': True})


if __name__ == '__main__':
    import configparser

    config = configparser.ConfigParser()
    config.read('alembic.ini')

    unittest.main()
