import unittest
import json
from flask_testing import TestCase
from flask import current_app

from app import create_app
from database import db

from models.user import User
from models.media import Media

from logic.user import add_user, get_user
from logic.media import upsert_media, add_media, update_media, remove_media, get_media


class GoGoMediaTestCase(TestCase):

    def create_app(self):
        return create_app(test=True)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class GoGoMediaModelTestCase(GoGoMediaTestCase):

    def test_add_user(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user in db.session)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, 'testname')

    def test_remove_user(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user in db.session)

        db.session.delete(user)
        db.session.commit()

        self.assertFalse(user in db.session)

    def test_user_get_id(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.get_id(), '1')

    def test_user_is_authenticated(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertFalse(user.is_authenticated())

        user.authenticated = True
        db.session.commit()

        self.assertTrue(user.is_authenticated())

    def test_user_is_active(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user.is_active())

    def test_user_is_anonymous(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertFalse(user.is_anonymous())

    def test_user_authenticate_password(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertFalse(user.authenticate_password('pass123'))
        self.assertTrue(user.authenticate_password('P@ssw0rd'))

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


class GoGoMediaLogicTestCase(GoGoMediaTestCase):

    def test_add_user(self):
        add_user('testname', 'P@ssw0rd')

        user = User.query.filter(User.username == 'testname').first()

        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testname')

    def test_get_user(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user, get_user('testname'))

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


class GoGoMediaViewTestCase(GoGoMediaTestCase):

    def test_index(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), 'Hello World')

    def test_user(self):
        response = self.client.post('/user',
                                    data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                                    content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 201)
        self.assertTrue(body['success'])
        self.assertIsInstance(body['auth_token'], str)

        user = User.query.filter(User.username == 'testname').first()

        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testname')

    def test_login(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertFalse(user.authenticated)

        with self.client:
            response = self.client.post('/login',
                                        data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                                        content_type='application/json')
            body = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            self.assertTrue(body['success'])
            self.assertTrue(user.authenticated)

    def test_invalid_login(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        self.assertFalse(user.authenticated)

        with self.client:
            response = self.client.post('/login',
                                        data=json.dumps({'username': 'testname', 'password': 'pass123'}),
                                        content_type='application/json')
            body = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            self.assertFalse(body['success'])
            self.assertFalse(user.authenticated)

    def test_logout(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        with self.client:
            self.client.post('/login',
                             data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                             content_type='application/json')

            response = self.client.get('/logout')
            body = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            self.assertTrue(body['success'])
            self.assertFalse(user.authenticated)

    def test_add_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame'}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'],
                         {'name': 'testmedianame', 'consumed': False})

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertFalse(media.consumed)

    def test_login_required_media_endpoint(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        # temporarily enable login for this test
        current_app.config['LOGIN_DISABLED'] = False

        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        with self.client:
            # havn't logged in yet
            response = self.client.put('/user/testname/media',
                                       data=json.dumps({'name': 'testmedianame'}),
                                       content_type='application/json')
            body = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            self.assertFalse(body['success'])
            self.assertEqual(body['message'],
                             'You are not logged in as this user. Please log in.')
            self.assertEqual(user.media, [])

            self.client.post('/login',
                             data=json.dumps({'username': 'testname', 'password': 'P@ssw0rd'}),
                             content_type='application/json')
            self.assertTrue(user.authenticated)

            # have logged in
            response = self.client.put('/user/testname/media',
                                       data=json.dumps({'name': 'testmedianame'}),
                                       content_type='application/json')
            body = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            self.assertTrue(body['success'])
            self.assertEqual(body['data'],
                             {'name': 'testmedianame', 'consumed': False})
            media_list = get_media('testname')
            self.assertEqual(media_list, [{'name': 'testmedianame', 'consumed': False}])

    def test_login_required_media_endpoint_different_user(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        # temporarily enable login for this test
        current_app.config['LOGIN_DISABLED'] = False

        user1 = User('testname1', 'P@ssw0rd')
        user2 = User('testname2', 'pass123')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        with self.client:
            self.client.post('/login',
                             data=json.dumps({'username': 'testname1', 'password': 'P@ssw0rd'}),
                             content_type='application/json')

            self.assertTrue(user1.authenticated)

            response = self.client.put('/user/testname2/media',
                                       data=json.dumps({'name': 'testmedianame'}),
                                       content_type='application/json')
            body = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            self.assertFalse(body['success'])
            self.assertEqual(body['message'], 'You are not logged in as this user. Please log in.')

            media_list = get_media('testname2')
            self.assertEqual(media_list, [])

    def test_nonexistent_user_media_endpoint(self):
        """
        This test applies to all the media functions that use the /user/<username>/media endpoint
        """
        with self.client:
            response = self.client.put('/user/testname/media',
                                       data=json.dumps({'name': 'testmedianame'}),
                                       content_type='application/json')
            body = json.loads(response.get_data(as_text=True))

            self.assertEqual(response.status_code, 200)
            self.assertFalse(body['success'])
            self.assertEqual(body['message'],
                             'User doesn\'t exist. Please register user.')

    def test_add_media_consumed(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed': True}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'],
                         {'name': 'testmedianame', 'consumed': True})

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertTrue(media.consumed)

    def test_add_media_unconsumed(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed': False}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], {'name': 'testmedianame', 'consumed': False})

        media = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).first()

        self.assertIsNotNone(media)
        self.assertEqual(media.medianame, 'testmedianame')
        self.assertEqual(media.user, user.id)
        self.assertFalse(media.consumed)

    def test_update_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id, consumed=False)
        db.session.add(media)
        db.session.commit()

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed': True}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'],
                         {'name': 'testmedianame', 'consumed': True})

        media_list = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertTrue(media_list[0].consumed)

        response = self.client.put('/user/testname/media',
                                   data=json.dumps({'name': 'testmedianame', 'consumed': False}),
                                   content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(body['data'],
                         {'name': 'testmedianame', 'consumed': False})

        media_list = Media.query.filter((Media.user == user.id) & (Media.medianame == 'testmedianame')).all()

        self.assertEqual(len(media_list), 1)
        self.assertEqual(media_list, [media])
        self.assertFalse(media_list[0].consumed)

    def test_get_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media1 = Media('testmedianame1', user.id)
        media2 = Media('testmedianame2', user.id)
        db.session.add(media1)
        db.session.add(media2)
        db.session.commit()

        response = self.client.get('/user/testname/media')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(sorted(body['data'], key=lambda media: media['name']),
                         [{'name': 'testmedianame1', 'consumed': False},
                          {'name': 'testmedianame2', 'consumed': False}])

    def test_get_consumed_media(self):
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

        response = self.client.get('/user/testname/media?consumed=yes')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(sorted(body['data'], key=lambda media: media['name']),
                         [{'name': 'testmedianame1', 'consumed': True},
                          {'name': 'testmedianame2', 'consumed': True},
                          {'name': 'testmedianame5', 'consumed': True}])

    def test_get_unconsumed_media(self):
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

        response = self.client.get('/user/testname/media?consumed=no')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])
        self.assertEqual(sorted(body['data'], key=lambda media: media['name']),
                         [{'name': 'testmedianame3', 'consumed': False},
                          {'name': 'testmedianame4', 'consumed': False}])

    def test_delete_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        media = Media('testmedianame', user.id)
        db.session.add(media)
        db.session.commit()

        response = self.client.delete('/user/testname/media',
                                      data=json.dumps({'name': 'testmedianame'}),
                                      content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])

        media_list = Media.query.filter(Media.user == user.id).all()

        self.assertEqual(media_list, [])

    def test_delete_unexisting_media(self):
        user = User('testname', 'P@ssw0rd')
        db.session.add(user)
        db.session.commit()

        response = self.client.delete('/user/testname/media',
                                      data=json.dumps({'name': 'testmedianame'}),
                                      content_type='application/json')
        body = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(body['success'])


if __name__ == '__main__':
    # import configparser

    # config = configparser.ConfigParser()
    # config.read('alembic.ini')

    unittest.main()
